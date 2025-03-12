import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/yelp_restaurants.db")

# 目标城市列表
TARGET_CITIES = ["Tokyo", "Montreal", "New York", "Paris", "London"]

# ✅ Tokyo 所有区的列表
TOKYO_DISTRICTS = [
    "Chūō", "Chiyoda", "Minato", "Shinjuku", "Shibuya", "Taitō", "Sumida", "Kōtō",
    "Shinagawa", "Meguro", "Ōta", "Setagaya", "Suginami", "Nakano", "Toshima",
    "Kita", "Arakawa", "Itabashi", "Nerima", "Adachi", "Katsushika", "Edogawa"
]

# ✅ New York 相关地区
NEW_YORK_DISTRICTS = ["Brooklyn", "Astoria", "Long Island City", "Queens", "Bronx", "Manhattan", "Staten Island"]

# ✅ London 相关地区
LONDON_DISTRICTS = ["Covent Garden", "Kensington", "Knightsbridge", "Westminster", "Camden", "Soho", "Chelsea"]

def standardize_city(city, state, country):
    """ 归一化城市名称 """
    city = city.lower()  # 统一转小写，避免大小写问题
    state = state.lower() if state else ""
    country = country.lower() if country else ""

    # **归类到 Tokyo**
    if city in [d.lower() for d in TOKYO_DISTRICTS] or "tokyo" in city or "shibuya" in city or "shinjuku" in city:
        return "Tokyo"

    # **归类到 New York**
    elif city in [d.lower() for d in NEW_YORK_DISTRICTS] or "new york" in city:
        return "New York"

    # **归类到 London**
    elif city in [d.lower() for d in LONDON_DISTRICTS] or "london" in city:
        return "London"

    # **归类到 Montreal**
    elif "montreal" in city:
        return "Montreal"

    # **归类到 Paris**
    elif "paris" in city:
        return "Paris"

    else:
        return "Other"  # 不在目标城市的归为 "Other"

def clean_data():
    """ 清理数据库数据 """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # **更新 locations 里的 city**
    cursor.execute("SELECT location_id, city, state, country FROM locations")
    locations = cursor.fetchall()

    for location_id, city, state, country in locations:
        standardized_city = standardize_city(city, state, country)
        cursor.execute("UPDATE locations SET city = ? WHERE location_id = ?", (standardized_city, location_id))

    # **删除不在目标城市的记录**
    cursor.execute("DELETE FROM locations WHERE city = 'Other'")
    cursor.execute("DELETE FROM restaurants WHERE location_id NOT IN (SELECT location_id FROM locations)")

    conn.commit()
    conn.close()
    print("✅ 位置数据清理完成！")

if __name__ == "__main__":
    clean_data()
