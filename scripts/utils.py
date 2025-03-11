def get_location_id(cursor, city, address, latitude, longitude):
    """ 获取或创建 location_id """
    cursor.execute("SELECT location_id FROM locations WHERE address = ?", (address,))
    row = cursor.fetchone()
    if row:
        return row[0]

    cursor.execute("""
    INSERT INTO locations (city, country, address, latitude, longitude)
    VALUES (?, ?, ?, ?, ?)
    """, (city, "Unknown", address, latitude, longitude))

    return cursor.lastrowid


def get_category_id(cursor, categories):
    """ 获取或创建 category_id（取第一个类别） """
    if not categories:
        return None
    category_name = categories[0]["title"]

    cursor.execute("SELECT category_id FROM categories WHERE category_name = ?", (category_name,))
    row = cursor.fetchone()
    if row:
        return row[0]

    cursor.execute("INSERT INTO categories (category_name) VALUES (?)", (category_name,))
    return cursor.lastrowid
