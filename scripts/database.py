import sqlite3
import os

def create_database():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/yelp_restaurants.db")

    # 确保 data 目录存在    if not os.path.exists("data"):
    #         os.makedirs("data")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 创建餐厅表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS restaurants (
        restaurant_id TEXT PRIMARY KEY,
        name TEXT,
        rating REAL,
        price TEXT,
        category_id INTEGER,
        location_id INTEGER
    )
    """)

    # 创建地理位置表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations (
        location_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        state TEXT,
        country TEXT,
        address TEXT,
        postal_code TEXT,
        latitude REAL,
        longitude REAL
    )
    """)

    # 创建餐厅类别表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT UNIQUE
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("✅ SQLite 数据库初始化完成！")
