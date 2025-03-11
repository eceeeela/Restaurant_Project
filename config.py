import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件

API_KEY = os.getenv("YELP_API_KEY")
CLIENT_ID = os.getenv("YELP_CLIENT_ID")

CITIES = ['Montreal', 'New York', 'Tokyo', 'Paris', 'London']
CATEGORIES = ['chinese', 'japanese', 'korean', 'italian',
              'french', 'spanish', 'mexican', 'vietnamese',
              'british', 'american']
RECORDS_PER_CATEGORY = 200
