import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

def test_bot():
    if not TOKEN:
        print("Error: No token found in .env")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/getMe"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data['ok']:
                bot_user = data['result']
                print(f"SUCCESS: Bot found! @{bot_user['username']} (ID: {bot_user['id']})")
                print(f"Name: {bot_user['first_name']}")
            else:
                print(f"FAILED: Telegram returned ok=False. {data}")
        else:
            print(f"FAILED: HTTP {response.status_code}")
    except Exception as e:
        print(f"Error connecting: {e}")

if __name__ == "__main__":
    test_bot()
