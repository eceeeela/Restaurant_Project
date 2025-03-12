import os
from scripts.yelp_scraper import run_scraper
from scripts.data_cleaning import clean_data
from scripts.database import create_database

# 数据库路径
DB_PATH = "data/yelp_restaurants.db"


def reset_database():
    """ 删除并重新创建数据库 """
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("🗑️ 已删除旧数据库")

    create_database()
    print("✅ 重新创建数据库成功！")


def main():
    """ 统一执行 Yelp 数据爬取和清理 """
    print("🚀 Yelp 数据爬取 & 清理启动！")

    reset_database()

    print("📡 开始爬取 Yelp 数据...")
    run_scraper()
    print("✅ Yelp 数据爬取完成！")

    print("🧹 开始清理 Yelp 数据...")
    clean_data()
    print("✅ 数据清理完成！")

    print("🎉 所有任务完成！")


if __name__ == "__main__":
    main()
