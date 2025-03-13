# 📊 Yelp Restaurant Data Analysis

### 🔍 Overview
This project collects, cleans, and analyzes restaurant data from **Yelp** using the Yelp API. The goal is to **compare restaurants within and across multiple cities**, focusing on **categories, prices, ratings, and locations**.

The project involves:
- **Scraping data** from the Yelp API.
- **Storing structured data** in an SQLite database.
- **Cleaning & standardizing data** (handling missing values, duplicate entries, price normalization, category mapping, etc.).
- **Analyzing the data** using **Power BI dashboards**.
- **Visualizing restaurant distributions** using maps, bar charts, and pie charts.

---

## 🚀 Features
### ✅ **Data Collection**
- Fetches restaurant details from **Yelp API** for:
  - **Cities**: Montreal, New York, Tokyo, Paris, London.
  - **Categories**: Chinese, Japanese, Korean, Italian, French, Spanish, Mexican, Vietnamese, British, American.
- Extracts **restaurant name, category, rating, price, location (lat/lon), review count, and address**.

### ✅ **Database Structure**
- **SQLite Database (`yelp_restaurants.db`)**
- **Tables**:
  - **restaurants** → Stores restaurant details.
  - **locations** → Stores city, state, country, address, lat/lon.
  - **categories** → Standardized restaurant categories.

### ✅ **Data Cleaning**
- Converts **categories into a standardized format**.
- Filters **N/A prices, extreme ratings (too high/too low)**.
- Removes **duplicate restaurants (same name + address)**.
- Normalizes **price levels across different currencies**.
- Groups **district-based city names into standard city names**.

### ✅ **Data Analysis & Visualization**
- **Dashboard 1**: **Single City Analysis**
  - 🏙️ **Restaurant count per category**.
  - ⭐ **Average rating per category**.
  - 💰 **Price distribution** (Pie chart).
  - 🗺️ **Map visualization** (Restaurant locations, colored by rating/price).
![image](https://github.com/eceeeela/Restaurant_Project/blob/main/img/demoPic.png)
  
- **Dashboard 2**: **Multi-City Comparison**
  - 📌 **Comparing different cities’ price levels**.
  - 🍽️ **Which cuisine is most popular in each city?**
  - 📊 **Which city has the highest-rated restaurants?**


## 🛠️ Project Structure
```
yelp_restaurant_analysis/
│
├── data/                    
│   ├── raw_data/            # Stores raw data from Yelp API
│   ├── yelp_restaurants.db  # SQLite database
│   ├── cleaned_data.csv     # Cleaned data for Power BI
│   └── Screenshot_2025-03-11_Montreal_Dashboard.png  # Dashboard image
│
├── scripts/                 
│   ├── scraper.py           # Scrapes Yelp data
│   ├── data_cleaning.py     # Cleans and processes data
│   ├── database.py          # Creates and manages database
│   ├── utils.py             # Helper functions for DB & data processing
│
├── notebooks/               
│   ├── data_exploration.ipynb  # Jupyter Notebook for initial data analysis
│
├── dashboards/              
│   ├── dashboard_city.pbix  # Power BI: Single city analysis
│   ├── dashboard_comparison.pbix  # Power BI: Multi-city comparison
│
├── config.py                # API keys & configuration
├── main.py                  # Runs the full pipeline (scraping → cleaning → storing)
├── requirements.txt         # Required Python packages
├── README.md                # Project documentation
└── .env                     # Stores API keys (excluded from Git)
```

---

## 🔧 Installation & Setup
### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/your-username/yelp-restaurant-analysis.git
cd yelp-restaurant-analysis
```

### 2️⃣ **Install Dependencies**
```
pip install -r requirements.txt
```

### 3️⃣ **Set Up API Keys**
- Create a `.env` file in the root directory and add:
```ini
YELP_API_KEY=your_yelp_api_key
```

### 4️⃣ **Run Data Collection**
```
python main.py
```
This will:

✅ Scrape restaurant data  
✅ Store it in SQLite  
✅ Clean and preprocess the data  

### 5️⃣ **Analyze in Power BI**
- Open **Power BI**.
- Load `cleaned_data.csv` or connect to `yelp_restaurants.db`.
- Use **dashboards/dashboard_city.pbix** and **dashboards/dashboard_comparison.pbix** to visualize.

---

## 📊 Sample Dashboards
### **Dashboard 1: Single City Analysis**
- 📍 **Map of restaurants by rating/price**.
- 🍽️ **Cuisine distribution**.
- ⭐ **Best & worst rated categories**.
  
### **Dashboard 2: Multi-City Comparison**
- 🌎 **Comparing price levels across cities**.
- 🥇 **Which city has the best-rated restaurants?**
- 🍔 **Which cuisine is dominant in each city?**

---

## 🎯 Future Improvements
- 🌍 **Expand to more cities & cuisines**.
- 🤖 **Automate monthly data updates**.
- 📈 **Advanced analytics (sentiment analysis on reviews, restaurant trends, etc.)**.

---

## 🏆 Credits
**Tools Used**: Python, SQLite, Power BI, Pandas, Yelp API, Bing Maps
