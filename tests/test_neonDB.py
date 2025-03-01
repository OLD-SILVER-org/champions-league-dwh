

import os
import sys
from dotenv import load_dotenv

# Thêm thư mục 'database' vào sys.path
database_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__), '../database'))
print(f"Adding {database_path} to sys.path")
sys.path.append(database_path)

# Kiểm tra xem đường dẫn đã được thêm vào sys.path chưa
print("Current sys.path:")
for path in sys.path:
    print(path)
from neon import NeonStagingDB as neon
load_dotenv()
# Kiểm tra xem biến môi trường NEON_URL đã được tải chưa
neon_url = os.getenv("NEON_URL")
print(f"NEON_URL: {neon_url}")


class TestNeon():
    def __init__(self):
        self.db = neon()  # Khởi tạo đối tượng NeonStagingDB
        pass

    def connect(self):
        self.db.connect()  # Kết nối đến cơ sở dữ liệu
    pass

    def close(self):
        self.db.close()  # Đóng kết nối cơ sở dữ liệu
    pass


# Example usage
if __name__ == "__main__":
    test = TestNeon()
    test.connect()
    test.close()
