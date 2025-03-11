import os
import sqlite3
from scripts.yelp_scraper import run_scraper
from scripts.database import create_database

# 获取数据库路径
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/yelp_restaurants.db")

def check_database_exists():
    """ 检查数据库是否存在 """
    return os.path.exists(DB_PATH)

def main():
    print("🚀 Yelp 餐厅数据爬取程序启动！")

    # 如果数据库不存在，先创建数据库
    if not check_database_exists():
        print("🔧 数据库未找到，正在初始化...")
        create_database()
        print("✅ 数据库创建完成！")

    # 运行 Yelp 爬虫
    run_scraper()

    print("🎉 Yelp 数据爬取完成，数据已存入数据库！")

if __name__ == "__main__":
    main()
