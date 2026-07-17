# BTC Tracker
import requests
import json
import os
import csv
import logging
from datetime import datetime

API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
JSON_FILE = "bitcoin_prices.json"
CSV_FILE = "bitcoin_prices.csv"

# تنظیمات لاگ
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    # دریافت قیمت بیت‌کوین
    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()

    price = response.json()["bitcoin"]["usd"]

    # ایجاد رکورد جدید
    new_record = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "price_usd": price
    }

    # ذخیره در JSON
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    data.append(new_record)

    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    # ذخیره در CSV (Append Mode)
    file_exists = os.path.exists(CSV_FILE)

    with open(CSV_FILE, "a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["timestamp", "price_usd"])

        if not file_exists:
            writer.writeheader()

        writer.writerow(new_record)

    logging.info(f"Price saved successfully: {new_record}")

except requests.exceptions.ConnectionError:
    logging.error("Connection Error: Unable to connect to API.")

except requests.exceptions.Timeout:
    logging.error("Timeout Error: API did not respond within 10 seconds.")

except Exception as e:
    logging.error(f"Unexpected Error: {e}")