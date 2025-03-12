import sqlite3


def get_location_id(cursor, city, country, address, latitude, longitude):
    """ 获取或创建 location_id，确保地址唯一性 """
    cursor.execute("SELECT location_id FROM locations WHERE address = ?", (address,))
    row = cursor.fetchone()
    if row:
        return row[0]  # 返回已存在的 location_id

    # 插入新地址
    cursor.execute("""
    INSERT INTO locations (city, country, address, latitude, longitude)
    VALUES (?, ?, ?, ?, ?)
    """, (city, country, address, latitude, longitude))

    return cursor.lastrowid  # 返回新插入的 location_id


def get_category_id(cursor, primary_category):
    """ 获取或创建 category_id，确保类别唯一 """
    if not primary_category:
        return None

    primary_category = primary_category.title()  # 统一首字母大写

    cursor.execute("SELECT category_id FROM categories WHERE category_name = ?", (primary_category,))
    row = cursor.fetchone()
    if row:
        return row[0]  # 返回已存在的 category_id

    # 插入新类别
    cursor.execute("INSERT INTO categories (category_name) VALUES (?)", (primary_category,))
    return cursor.lastrowid  # 返回新插入的 category_id
