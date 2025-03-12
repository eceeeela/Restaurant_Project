import sqlite3
import os

def create_database():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/yelp_restaurants.db")

    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # ✅ 创建 categories 表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT UNIQUE
    )
    """)

    # ✅ 创建 locations 表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS locations (
        location_id INTEGER PRIMARY KEY AUTOINCREMENT,
        city TEXT,
        state TEXT,
        country TEXT,
        address TEXT UNIQUE,
        zip_code TEXT,
        latitude REAL,
        longitude REAL
    )
    """)

    # ✅ 创建 restaurants 表
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS restaurants (
        restaurant_id TEXT PRIMARY KEY,
        name TEXT,
        rating REAL CHECK (rating BETWEEN 1 AND 5),
        price TEXT,
        review_count INTEGER DEFAULT 0,
        categories TEXT,
        primary_category TEXT,
        category_id INTEGER,
        location_id INTEGER,
        latitude REAL,
        longitude REAL,
        FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE SET NULL,
        FOREIGN KEY (location_id) REFERENCES locations(location_id) ON DELETE CASCADE
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("✅ SQLite 数据库初始化完成！")
