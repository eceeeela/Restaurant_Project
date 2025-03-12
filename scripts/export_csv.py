import sqlite3
import pandas as pd
import os

# 定义数据库和 CSV 路径
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/yelp_restaurants.db")
CSV_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/csv_exports/")

# 确保 CSV 目录存在
os.makedirs(CSV_DIR, exist_ok=True)

# 连接数据库
conn = sqlite3.connect(DB_PATH)

# 要导出的表
tables = ["restaurants", "locations", "categories"]

for table in tables:
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    csv_path = os.path.join(CSV_DIR, f"{table}.csv")
    df.to_csv(csv_path, index=False)
    print(f"✅ 数据表 {table} 导出完成：{csv_path}")

conn.close()
print("🎉 所有数据已导出到 CSV！")
