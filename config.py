import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件

API_KEY = os.getenv("YELP_API_KEY")
CLIENT_ID = os.getenv("YELP_CLIENT_ID")

CITIES = ['Montreal', 'New York', 'Tokyo', 'Paris']
CATEGORIES = ['chinese', 'japanese', 'korean', 'italian', 'french', 'spanish']
RECORDS_PER_CATEGORY = 150  # 每个类别爬取 150 条数据
