import openpyxl
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .models import Department, Position, Employee
from .forms import DepartmentForm, PositionForm, EmployeeForm
from .serializers import DepartmentSerializer, MyTokenObtainPairSerializer, PositionSerializer, EmployeeSerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg import openapi

# For CSV export
import csv
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes

# REST API Views

# Department API Views
class DepartmentListCreateView(ListCreateAPIView):
    queryset = Department.objects.all().order_by('id')
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

class DepartmentRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

# Position API Views
class PositionListCreateView(ListCreateAPIView):
    queryset = Position.objects.all().order_by('id')
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]

class PositionRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [IsAuthenticated]

# Employee API Views
class EmployeeListCreateView(ListCreateAPIView):
    queryset = Employee.objects.select_related('department', 'position').all().order_by('id')
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['department', 'position', 'date_of_joining']
    search_fields = ['first_name', 'last_name', 'email', 'phone_number']
    ordering_fields = '__all__'

    @swagger_auto_schema(operation_summary="List and create employees")
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Create a new employee")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class EmployeeRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.select_related('department', 'position').all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    
class EmployeeExportExcelView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        employees = Employee.objects.select_related('department', 'position').all()

        # Create a workbook and sheet
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        sheet.title = 'Employees'

        # Define column headers
        headers = [
            'ID', 'First Name', 'Last Name', 'Email', 'Phone Number',
            'Date of Birth', 'Date of Joining', 'Salary',
            'Department', 'Position'
        ]
        sheet.append(headers)

        # Add data rows
        for emp in employees:
            sheet.append([
                emp.id,
                emp.first_name,
                emp.last_name,
                emp.email,
                emp.phone_number,
                emp.date_of_birth.strftime('%Y-%m-%d') if emp.date_of_birth else '',
                emp.date_of_joining.strftime('%Y-%m-%d') if emp.date_of_joining else '',
                emp.salary,
                emp.department.name if emp.department else '',
                emp.position.title if emp.position else '',
            ])

        # Create response
        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename="employees.xlsx"'
        workbook.save(response)
        return response

# Web Dashboard View
class HomeView(TemplateView):
    template_name = 'adminpanel/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'departments': Department.objects.all(),
            'positions': Position.objects.all(),
            'employees': Employee.objects.select_related('department', 'position').all(),
            'department_form': DepartmentForm(),
            'position_form': PositionForm(),
            'employee_form': EmployeeForm(),
        })
        return context

    def post(self, request, *args, **kwargs):
        if 'add_department' in request.POST:
            form = DepartmentForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')

        elif 'add_position' in request.POST:
            form = PositionForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')

        elif 'add_employee' in request.POST:
            form = EmployeeForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')

        return self.get(request, *args, **kwargs)

# CSV Export API View
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_employees_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employees.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'ID', 'First Name', 'Last Name', 'Email', 'Phone Number',
        'Date of Birth', 'Date of Joining', 'Salary',
        'Department', 'Position'
    ])

    employees = Employee.objects.select_related('department', 'position').all()

    for emp in employees:
        writer.writerow([
            emp.id,
            emp.first_name,
            emp.last_name,
            emp.email,
            emp.phone_number,
            emp.date_of_birth,
            emp.date_of_joining,
            emp.salary,
            emp.department.name if emp.department else '',
            emp.position.title if emp.position else '',
        ])

    return response

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request):
        return super().post(request)
