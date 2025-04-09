import pandas as pd

# Path to your CSV file
file_path = r"F:\Python Projects\Sabhyasha Retail Tech\archive\employee_records.csv"

# Load the CSV file
df = pd.read_csv(file_path)

# Print column names
print("CSV Columns:", df.columns.tolist())
