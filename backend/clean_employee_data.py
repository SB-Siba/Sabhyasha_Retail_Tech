import pandas as pd
import os
from faker import Faker

# Initialize Faker
fake = Faker()
Faker.seed(42)

# File paths
input_file = r"F:\Python Projects\Sabhyasha Retail Tech\archive\employee_records.csv"
output_file = r"F:\Python Projects\Sabhyasha Retail Tech\archive\cleaned_employee_records.csv"

# Load CSV
df = pd.read_csv(input_file)

# Split names
df[['first_name', 'last_name']] = df['Employee_Name'].str.split(' ', n=1, expand=True)

# Track used emails to ensure uniqueness
used_emails = set()
emails = []

for i, row in df.iterrows():
    base_email = f"{row['first_name'].lower()}.{row['last_name'].lower()}@example.com"
    email = base_email
    counter = 1

    while email in used_emails:
        email = f"{row['first_name'].lower()}.{row['last_name'].lower()}{counter}@example.com"
        counter += 1

    used_emails.add(email)
    emails.append(email)

df['email'] = emails

# Generate unique phone numbers
df['phone_number'] = [fake.unique.msisdn()[:10] for _ in range(len(df))]

# Add random realistic date_of_birth
df['date_of_birth'] = [fake.date_of_birth(minimum_age=22, maximum_age=60) for _ in range(len(df))]

# Rename columns to match model
df.rename(columns={
    'Joining_Date': 'date_of_joining',
    'Salary': 'salary',
    'Department': 'department',
    'Position': 'position'
}, inplace=True)

# Select required fields
df = df[['first_name', 'last_name', 'email', 'phone_number', 'date_of_birth', 'date_of_joining', 'salary', 'department', 'position']]

# Save
df.to_csv(output_file, index=False)
print(f"✅ Data cleaned and saved: {output_file}")
