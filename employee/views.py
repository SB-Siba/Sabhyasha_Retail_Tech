from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated
from .models import Department, Position, Employee
from .serializers import EmployeeSerializer
from .serializers import DepartmentSerializer, PositionSerializer, EmployeeSerializer



class DepartmentListCreateApi(APIView):
   
    @swagger_auto_schema(
        operation_description="List all departments",
        responses={200: DepartmentSerializer(many=True)}
    )
    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=DepartmentSerializer,
        operation_description="Create a new department",
        responses={201: DepartmentSerializer()}
    )
    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class DepartmentDetailApi(APIView):
 
    def get_object(self, pk):
        try:
            return Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Retrieve department by ID",
        responses={200: DepartmentSerializer()}
    )
    def get(self, request, pk):
        department = self.get_object(pk)
        if not department:
            return Response({"error": "Not found"}, status=404)
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=DepartmentSerializer,
        operation_description="Update department",
        responses={200: DepartmentSerializer()}
    )
    def put(self, request, pk):
        department = self.get_object(pk)
        if not department:
            return Response({"error": "Not found"}, status=404)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_description="Delete department",
        responses={204: "Deleted successfully"}
    )
    def delete(self, request, pk):
        department = self.get_object(pk)
        if not department:
            return Response({"error": "Not found"}, status=404)
        department.delete()
        return Response(status=204)


class DepartmentListCreateApi(APIView):

    @swagger_auto_schema(
        operation_description="List all departments",
        responses={200: DepartmentSerializer(many=True)}
    )
    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=DepartmentSerializer,
        operation_description="Create a new department",
        responses={201: DepartmentSerializer()}
    )
    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class DepartmentDetailApi(APIView):
 
    def get_object(self, pk):
        try:
            return Department.objects.get(pk=pk)
        except Department.DoesNotExist:
            return None

    @swagger_auto_schema(
        operation_description="Retrieve department by ID",
        responses={200: DepartmentSerializer()}
    )
    def get(self, request, pk):
        department = self.get_object(pk)
        if not department:
            return Response({"error": "Not found"}, status=404)
        serializer = DepartmentSerializer(department)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=DepartmentSerializer,
        operation_description="Update department",
        responses={200: DepartmentSerializer()}
    )
    def put(self, request, pk):
        department = self.get_object(pk)
        if not department:
            return Response({"error": "Not found"}, status=404)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_description="Delete department",
        responses={204: "Deleted successfully"}
    )
    def delete(self, request, pk):
        department = self.get_object(pk)
        if not department:
            return Response({"error": "Not found"}, status=404)
        department.delete()
        return Response(status=204)


class PositionListCreateApi(APIView):
 
    @swagger_auto_schema(operation_description="List all positions", responses={200: PositionSerializer(many=True)})
    def get(self, request):
        positions = Position.objects.all()
        serializer = PositionSerializer(positions, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=PositionSerializer, operation_description="Create new position", responses={201: PositionSerializer()})
    def post(self, request):
        serializer = PositionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PositionDetailApi(APIView):
  
    def get_object(self, pk):
        try:
            return Position.objects.get(pk=pk)
        except Position.DoesNotExist:
            return None

    @swagger_auto_schema(operation_description="Retrieve position by ID", responses={200: PositionSerializer()})
    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)
        serializer = PositionSerializer(obj)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=PositionSerializer, operation_description="Update position", responses={200: PositionSerializer()})
    def put(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)
        serializer = PositionSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(operation_description="Delete position", responses={204: "Deleted"})
    def delete(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)
        obj.delete()
        return Response(status=204)


class EmployeeListCreateApi(APIView):
 
    @swagger_auto_schema(operation_description="List all employees", responses={200: EmployeeSerializer(many=True)})
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=EmployeeSerializer, operation_description="Create employee", responses={201: EmployeeSerializer()})
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class EmployeeDetailApi(APIView):

    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            return None

    @swagger_auto_schema(operation_description="Retrieve employee", responses={200: EmployeeSerializer()})
    def get(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)
        serializer = EmployeeSerializer(obj)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=EmployeeSerializer, operation_description="Update employee", responses={200: EmployeeSerializer()})
    def put(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)
        serializer = EmployeeSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(operation_description="Delete employee", responses={204: "Deleted"})
    def delete(self, request, pk):
        obj = self.get_object(pk)
        if not obj:
            return Response({"error": "Not found"}, status=404)
        obj.delete()
        return Response(status=204)
