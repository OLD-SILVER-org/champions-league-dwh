import pandas as pd

file_path = "./data/processed/fbref_data/Champions-League/SCORE_AND_FIXTURES/2024/2025-02-28_23-37-19.csv"

df = pd.read_csv(file_path)

df = pd.read_csv(file_path, delimiter=",")
# Chọn và in các cột mong muốn
selected_columns = ["home", "away", "xg_home",
                    "xg_away", "home_score", "away_score", "attendance"]
print(df[selected_columns].head(10))  # In 10 dòng đầu
print("---------------------")
for i, row in df.iterrows():
    print(row.tolist())  # In từng dòng dưới dạng list
    if i == 10:  # Chỉ in thử 10 dòng
        break
