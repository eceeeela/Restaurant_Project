import requests
import sqlite3
import os
import time
from urllib.parse import urlencode
from config import API_KEY, CITIES, CATEGORIES, RECORDS_PER_CATEGORY
from scripts.utils import get_location_id, get_category_id

# Yelp API 相关信息
BASE_URL = "https://api.yelp.com/v3/businesses/search"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# 获取数据库路径
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/yelp_restaurants.db")


def fetch_restaurants(city, category):
    """ 从 Yelp API 获取指定城市 & 类别的餐厅数据 """
    restaurants = []
    offset = 0
    limit = 50  # Yelp API 每次最多返回 50 条数据

    while offset < RECORDS_PER_CATEGORY:
        params = {
            "location": city,
            "categories": category,
            "limit": limit,
            "offset": offset,
        }
        url = f"{BASE_URL}?{urlencode(params)}"

        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"⚠️  获取 {city} - {category} 失败，状态码: {response.status_code}")
            return []  # 直接返回空列表

        data = response.json()
        businesses = data.get("businesses", [])
        restaurants.extend(businesses)

        if len(businesses) < limit:
            break  # 已经获取完所有数据，不需要继续请求下一页

        offset += limit
        time.sleep(1)  # 避免 API 速率限制

    return restaurants


def save_to_database(restaurants, city):
    """ 将爬取的餐厅数据存入 SQLite 数据库 """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for rest in restaurants:
        name = rest["name"]
        rating = rest.get("rating", 0)
        price = rest.get("price", "N/A")
        address = ", ".join(rest["location"].get("display_address", []))
        latitude = rest["coordinates"].get("latitude")
        longitude = rest["coordinates"].get("longitude")

        # 获取或创建 location_id
        location_id = get_location_id(cursor, city, address, latitude, longitude)

        # 获取或创建 category_id
        category_id = get_category_id(cursor, rest["categories"])

        # 生成唯一 restaurant_id
        restaurant_id = f"{city[:3].upper()}{str(hash(name))[:6]}"

        cursor.execute("""
        INSERT OR IGNORE INTO restaurants (restaurant_id, name, rating, price, category_id, location_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (restaurant_id, name, rating, price, category_id, location_id))

    conn.commit()
    conn.close()


def run_scraper():
    """ 主函数：遍历城市 & 类别，爬取 Yelp 数据 """
    for city in CITIES:
        for category in CATEGORIES:
            print(f"📡 爬取 {city} - {category} 数据中...")
            restaurants = fetch_restaurants(city, category)

            # 如果该类别的餐厅数量不足 150，仍然保存已有的数据
            if len(restaurants) < RECORDS_PER_CATEGORY:
                print(
                    f"⚠️ {city} - {category} 的餐厅不足 {RECORDS_PER_CATEGORY} 个（仅找到 {len(restaurants)} 个），保存已有数据并继续。")
                if restaurants:  # 如果有数据，则保存
                    save_to_database(restaurants, city)
                    print(f"✅ {len(restaurants)} 条数据存入数据库")
                continue  # 继续到下一个类别

            # 如果餐厅数量足够，直接保存
            save_to_database(restaurants, city)
            print(f"✅ {len(restaurants)} 条数据存入数据库")

    print("🎉 爬取任务完成！")