import os
import django
import re
from faker import Faker
from random import randint
from datetime import timedelta
from django.utils.timezone import now

# ✅ Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

# ✅ Import models after Django setup
from adminpanel.models import Employee, Position, Department  

fake = Faker()

def populate_employees(batch_size=10000, total_records=50000):  
    employees = []
    
    for _ in range(total_records):  
        phone_number = re.sub(r'\D', '', fake.phone_number())  
        phone_number = phone_number[:15]  

        # ✅ Ensure department exists
        department_name = fake.company()
        department, _ = Department.objects.get_or_create(
            name=department_name, 
            defaults={"location": fake.city()}  # ✅ Use defaults for non-unique fields
        )

        # ✅ Ensure position exists
        position_name = fake.job()
        position, _ = Position.objects.get_or_create(title=position_name)

        # ✅ Generate valid random data
        employee = Employee(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            phone_number=phone_number,
            email=fake.unique.email(),
            date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=60),
            date_of_joining=now() - timedelta(days=randint(30, 3650)),  
            salary=round(randint(30000, 200000) * 1.2, 2),  
            department=department,
            position=position,
        )
        employees.append(employee)

        # ✅ Bulk insert in batches
        if len(employees) >= batch_size:
            Employee.objects.bulk_create(employees)
            print(f"✅ Inserted {len(employees)} employees")
            employees.clear()  

    # ✅ Insert remaining employees (if any)
    if employees:
        Employee.objects.bulk_create(employees)
        print(f"✅ Inserted {len(employees)} employees (final batch)")

    print("🎉 Employee population completed!")

if __name__ == "__main__":
    populate_employees(total_records=250000)
