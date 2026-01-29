import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def scan_channels():
    print("SCANNING UPDATES...")
    try:
        resp = requests.get(f"{BASE_URL}/getUpdates", params={"allowed_updates": ["message", "channel_post"]})
        data = resp.json()
        
        if not data.get('ok'):
            print("API Error")
            return

        results = data.get('result', [])
        found_channels = {}

        for update in results:
            chat_id = None
            title = None
            
            # Check forwarded messages (Most reliable for private channels)
            if 'message' in update and 'forward_from_chat' in update['message']:
                chat = update['message']['forward_from_chat']
                chat_id = chat['id']
                title = chat.get('title', 'Unknown')
                found_channels[chat_id] = title
            
            # Check direct channel posts (If bot is already admin)
            if 'channel_post' in update:
                chat = update['channel_post']['chat']
                chat_id = chat['id']
                title = chat.get('title', 'Unknown')
                found_channels[chat_id] = title

        if found_channels:
            print("FOUND CHANNELS:")
            for cid, name in found_channels.items():
                print(f"ID: {cid} | Name: {name}")
        else:
            print("NO CHANNELS FOUND. Did you forward the messages?")

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    scan_channels()
