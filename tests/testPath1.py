import os
import sys

# Thêm thư mục 'tests' vào sys.path
tests_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
print(f"Adding {tests_path} to sys.path")
sys.path.append(tests_path)

# Thêm thư mục 'database' vào sys.path
database_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../database'))
print(f"Adding {database_path} to sys.path")
sys.path.append(database_path)
from testPathDatabase import some_function


# Kiểm tra xem đường dẫn đã được thêm vào sys.path chưa
print("Current sys.path:")
for path in sys.path:
    print(path)

# Import module từ testPathDatabase.py

# Example usage
if __name__ == "__main__":
    some_function()  # Gọi hàm từ module testPathDatabase
