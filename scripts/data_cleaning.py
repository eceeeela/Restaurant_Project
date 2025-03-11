import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/yelp_restaurants.db")

def remove_duplicates():
    """ 去重：删除同名但 ID 不同的餐厅 """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM restaurants
    WHERE rowid NOT IN (
        SELECT MIN(rowid) FROM restaurants GROUP BY name
    )
    """)

    conn.commit()
    conn.close()
    print("✅ 重复数据清理完成！")

if __name__ == "__main__":
    remove_duplicates()
