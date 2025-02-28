import pandas as pd

df = pd.read_csv(
    r"data\processed\fbref_data\Champions-League\SCORE_AND_FIXTURES\2024\2025-02-27_23-00-49.csv")
print(df.head())  # Kiểm tra xem có dữ liệu bị lệch cột không
print(df.columns)  # Xem danh sách cột có khớp với PostgreSQL không
