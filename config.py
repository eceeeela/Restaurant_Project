import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YELP_API_KEY")
CLIENT_ID = os.getenv("YELP_CLIENT_ID")

if not API_KEY:
    raise ValueError("🚨 Missing YELP_API_KEY in .env file!")
if not CLIENT_ID:
    raise ValueError("🚨 Missing YELP_CLIENT_ID in .env file!")

# 要爬取的城市
# CITIES = ['Montreal', 'New York', 'Tokyo', 'Paris', 'London']
CITIES = ['Montreal', 'New York', 'Tokyo', 'Paris', 'London']

# 城市类别
CATEGORIES = ['Chinese', 'Japanese', 'Korean', 'Italian',
              'French', 'Spanish', 'Mexican', 'Vietnamese']

# 每个类别的餐厅数量
RECORDS_PER_CATEGORY = 200
