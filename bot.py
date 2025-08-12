import os
import requests
import time
from datetime import datetime

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
FROM = "Ковель"
TO = "Ірпінь"
DATE = "2025-08-15"
CHECK_INTERVAL = 60  # каждые 5 минут

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.get(url, params={"chat_id": CHAT_ID, "text": text})

def check_tickets():
    url = "https://booking.uz.gov.ua/train_search/"
    payload = {"from": FROM, "to": TO, "date": DATE, "time": 0, "another_ec": 0}
    r = requests.get(url, params=payload)
    data = r.json()
    
    if data.get("data", {}).get("list"):
        for train in data["data"]["list"]:
            for car in train["types"]:
                if car["places"] > 0:
                    link = f"https://booking.uz.gov.ua/?from={FROM}&to={TO}&date={DATE}"
                    send_telegram(
                        f"🎫 Есть билеты!\n🚆 {train['num']} "
                        f"{train['from']['station']} → {train['to']['station']}\n"
                        f"Тип: {car['title']}\nМест: {car['places']}\n🔗 {link}"
                    )
                    return True
    return False

while True:
    try:
        print(f"[{datetime.now()}] Проверка...")
        if check_tickets():
            print("Билеты найдены! Уведомление отправлено.")
            break
    except Exception as e:
        print("Ошибка:", e)
    time.sleep(CHECK_INTERVAL)
