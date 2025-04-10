from django.urls import path
from . import views

app_name = "employee"

urlpatterns = [
    # Department CRUD
    path('departments/', views.DepartmentListCreateApi.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', views.DepartmentDetailApi.as_view(), name='department-detail'),

    # Position CRUD
    path('positions/', views.PositionListCreateApi.as_view(), name='position-list-create'),
    path('positions/<int:pk>/', views.PositionDetailApi.as_view(), name='position-detail'),

    # Employee CRUD
    path('employees/', views.EmployeeListCreateApi.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', views.EmployeeDetailApi.as_view(), name='employee-detail'),
]