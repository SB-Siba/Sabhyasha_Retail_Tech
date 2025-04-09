from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Prevent duplicate departments
    location = models.CharField(max_length=255, blank=True, null=True)  # Allow empty location
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'adminpanel'
        ordering = ['name']  # Departments will be ordered alphabetically

    def __str__(self):
        return self.name


class Position(models.Model):
    title = models.CharField(max_length=150, unique=True)  # Increased max length
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'adminpanel'
        ordering = ['title']  # Positions will be ordered alphabetically

    def __str__(self):
        return self.title


class Employee(models.Model):
    first_name = models.CharField(max_length=100, blank=False, null=False)
    last_name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(unique=True, db_index=True, blank=False, null=False)  # Indexed for faster queries
    phone_number = models.CharField(max_length=15, unique=True, db_index=True, blank=False, null=False)  # Indexed
    date_of_birth = models.DateField(blank=True, null=True)  # Made optional
    date_of_joining = models.DateField(db_index=True, blank=False, null=False)  # Indexed for faster filtering
    salary = models.DecimalField(max_digits=12, decimal_places=2, blank=False, null=False)  # Increased max_digits for larger salaries

    department = models.ForeignKey(Department, on_delete=models.PROTECT)  # Prevent accidental deletion
    position = models.ForeignKey(Position, on_delete=models.PROTECT)  # Prevent accidental deletion

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'adminpanel'
        ordering = ['-date_of_joining']  # Most recent employees first

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
