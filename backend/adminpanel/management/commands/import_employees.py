import csv
import os
from sqlite3 import IntegrityError
from django.core.management.base import BaseCommand
from adminpanel.models import Employee, Department, Position
from django.utils.dateparse import parse_date

BATCH_SIZE = 5000  # Number of records per bulk insert

class Command(BaseCommand):
    help = 'Import employee records from a CSV file (optimized for large datasets)'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the cleaned CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        if not os.path.exists(csv_file):
            self.stdout.write(self.style.ERROR(f"❌ File not found: {csv_file}"))
            return

        created_count = 0
        skipped_rows = 0
        employees_to_create = []
        seen_emails = set()  # ✅ Track duplicate emails in the file

        # Preload departments and positions to avoid duplicate queries
        departments = {dept.name: dept for dept in Department.objects.all()}
        positions = {pos.title: pos for pos in Position.objects.all()}

        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                try:
                    required_fields = ['first_name', 'last_name', 'email', 'phone_number', 'department', 'position']
                    if not all(row.get(field) for field in required_fields):
                        raise ValueError('Missing required fields')

                    # Clean and extract values
                    first_name = row['first_name'].strip()
                    last_name = row['last_name'].strip()
                    email = row['email'].strip()
                    phone_number = row['phone_number'].strip()
                    dob_str = row.get('date_of_birth', '').strip()
                    doj_str = row.get('date_of_joining', '').strip()
                    date_of_birth = parse_date(dob_str) if dob_str else None
                    date_of_joining = parse_date(doj_str) if doj_str else None
                    salary = float(row['salary']) if row.get('salary') else 0.0

                    # Skip if email already exists in DB
                    if Employee.objects.filter(email=email).exists():
                        raise ValueError(f"Duplicate email in DB: {email}")

                    # ✅ Skip if email already seen in current file
                    if email in seen_emails:
                        raise ValueError(f"Duplicate email in file: {email}")
                    seen_emails.add(email)

                    # Department (create if not exist)
                    dept_name = row['department'].strip()
                    if dept_name not in departments:
                        departments[dept_name] = Department.objects.create(name=dept_name, location="Unknown")
                    department = departments[dept_name]

                    # Position (create if not exist)
                    pos_title = row['position'].strip()
                    if pos_title not in positions:
                        positions[pos_title] = Position.objects.create(title=pos_title)
                    position = positions[pos_title]

                    # Create an Employee instance
                    employee = Employee(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        phone_number=phone_number,
                        date_of_birth=date_of_birth,
                        date_of_joining=date_of_joining,
                        salary=salary,
                        department=department,
                        position=position
                    )
                    employees_to_create.append(employee)

                    if len(employees_to_create) >= BATCH_SIZE:
                        Employee.objects.bulk_create(employees_to_create)
                        created_count += len(employees_to_create)
                        self.stdout.write(self.style.SUCCESS(f"✅ Inserted {created_count} records..."))
                        employees_to_create = []

                except Exception as e:
                    skipped_rows += 1
                    self.stdout.write(self.style.WARNING(
                        f"⚠️ Skipped row due to error: {e}\n"
                        f"🔍 Row keys: {list(row.keys())}\n"
                        f"📝 Raw row: {row}"
                    ))

        # Final batch insert
        if employees_to_create:
            try:
                Employee.objects.bulk_create(employees_to_create)
                created_count += len(employees_to_create)
            except IntegrityError as e:
                self.stdout.write(self.style.ERROR(f"❌ Final batch failed due to: {e}"))

        self.stdout.write(self.style.SUCCESS(f"✅ Done! Total: {created_count} employees imported."))
        self.stdout.write(self.style.WARNING(f"⚠️ Total Skipped Rows: {skipped_rows}"))
