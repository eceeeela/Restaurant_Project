import requests
import sqlite3
import os
import time
from urllib.parse import urlencode
from config import API_KEY, CITIES, CATEGORIES, RECORDS_PER_CATEGORY
from scripts.utils import get_location_id, get_category_id  # ✅ 从 utils.py 导入

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

    while len(restaurants) < RECORDS_PER_CATEGORY:
        params = {
            "location": city,
            "categories": category,
            "limit": limit,
            "offset": offset,
        }
        url = f"{BASE_URL}?{urlencode(params)}"

        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"⚠️ 获取 {city} - {category} 失败，状态码: {response.status_code}")
            break  # 遇到 API 失败就退出循环

        data = response.json()
        businesses = data.get("businesses", [])

        if not businesses:
            print(f"⚠️ {city} - {category} 没有更多商户，但已爬取 {len(restaurants)} 条数据。")
            break  # 不再请求下一页，但不会丢失已爬取数据

        for biz in businesses:
            location = biz.get("location", {})

            # ✅ 获取完整类别列表，标准化成 Title Case
            all_categories = [c["title"].title() for c in biz.get("categories", [])]

            # ✅ primary_category 选择 `CATEGORIES` 里匹配的第一个
            matched_categories = [c for c in all_categories if c.lower() in [cat.lower() for cat in CATEGORIES]]
            primary_category = matched_categories[0] if matched_categories else category.title()

            restaurants.append({
                "name": biz["name"],
                "rating": biz.get("rating", 0),
                "price": biz.get("price", "N/A"),
                "review_count": biz.get("review_count", 0),
                "categories": ", ".join(all_categories),  # 存所有类别
                "category": primary_category,  # 主要类别
                "city": location.get("city", "Unknown"),
                "state": location.get("state", "Unknown"),
                "zip_code": location.get("zip_code", "Unknown"),
                "country": location.get("country", "Unknown"),
                "address": location.get("address1", ""),
                "latitude": biz.get("coordinates", {}).get("latitude"),
                "longitude": biz.get("coordinates", {}).get("longitude"),
            })

        offset += limit
        time.sleep(1)  # 避免 API 速率限制

    return restaurants  # ✅ 返回已爬取的所有数据，不管是否到达目标数量

def save_to_database(restaurants, city):
    """ 将爬取的餐厅数据存入 SQLite 数据库 """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for rest in restaurants:
        name = rest.get("name", "Unknown")
        rating = rest.get("rating", 0)
        price = rest.get("price", "N/A")
        review_count = rest.get("review_count", 0)
        address = rest.get("address", "Unknown")
        latitude = rest.get("latitude", None)
        longitude = rest.get("longitude", None)

        # ✅ 确保获取 `country`
        country = rest.get("country", "Unknown")

        # ✅ 处理 categories
        all_categories = rest.get("categories", "")
        primary_category = rest.get("category", "")

        # ✅ 获取或创建 location_id
        location_id = get_location_id(cursor, rest["city"], country, address, latitude, longitude)

        # ✅ 获取或创建 category_id
        category_id = get_category_id(cursor, primary_category)

        # ✅ 生成唯一 restaurant_id
        restaurant_id = f"{city[:3].upper()}-{abs(hash(name)) % 1000000}"

        cursor.execute("""
        INSERT OR IGNORE INTO restaurants 
        (restaurant_id, name, rating, price, review_count, categories, primary_category, category_id, location_id, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (restaurant_id, name, rating, price, review_count, all_categories, primary_category, category_id, location_id, latitude, longitude))

    conn.commit()
    conn.close()


def run_scraper():
    """ 主函数：遍历城市 & 类别，爬取 Yelp 数据 """
    for city in CITIES:
        for category in CATEGORIES:
            print(f"📡 爬取 {city} - {category} 数据中...")
            restaurants = fetch_restaurants(city, category)

            if len(restaurants) < RECORDS_PER_CATEGORY:
                print(f"⚠️ {city} - {category} 仅找到 {len(restaurants)} 条数据（目标 {RECORDS_PER_CATEGORY}），但仍然保存。")

            save_to_database(restaurants, city)
            print(f"✅ {len(restaurants)} 条数据存入数据库")

    print("🎉 爬取任务完成！")
