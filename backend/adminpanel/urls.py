from django.urls import path
from .views import (
    DepartmentListCreateView, DepartmentRetrieveUpdateDestroyView, EmployeeExportExcelView,
    PositionListCreateView, PositionRetrieveUpdateDestroyView,
    EmployeeListCreateView, EmployeeRetrieveUpdateDestroyView, export_employees_csv
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

urlpatterns = [
    # Department Endpoints
    path('departments/', DepartmentListCreateView.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', DepartmentRetrieveUpdateDestroyView.as_view(), name='department-detail'),

    # Position Endpoints
    path('positions/', PositionListCreateView.as_view(), name='position-list-create'),
    path('positions/<int:pk>/', PositionRetrieveUpdateDestroyView.as_view(), name='position-detail'),

    # Employee Endpoints
    path('employees/', EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', EmployeeRetrieveUpdateDestroyView.as_view(), name='employee-detail'),
    path('employees/export/csv/', export_employees_csv, name='employee-export-csv'),
    path('employees/export/excel/', EmployeeExportExcelView.as_view(), name='employees_export_excel'),
]
