from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    date_of_joining = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='employees')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone_number']),
            models.Index(fields=['date_of_joining']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
