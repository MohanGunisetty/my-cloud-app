import requests
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
STORAGE_ID = os.getenv('TELEGRAM_STORAGE_CHANNEL_ID')
METADATA_ID = os.getenv('TELEGRAM_METADATA_CHANNEL_ID')
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def final_verify():
    print(f"Verifying Storage ({STORAGE_ID})...")
    files = {'document': ('test.txt', b'Storage Test')}
    r1 = requests.post(f"{BASE_URL}/sendDocument", data={'chat_id': STORAGE_ID}, files=files)
    if r1.json().get('ok'):
        print("Storage: OK")
    else:
        print(f"Storage: FAIL - {r1.text}")

    print(f"Verifying Metadata ({METADATA_ID})...")
    r2 = requests.post(f"{BASE_URL}/sendMessage", json={'chat_id': METADATA_ID, 'text': 'Metadata Test'})
    if r2.json().get('ok'):
        print("Metadata: OK")
    else:
        print(f"Metadata: FAIL - {r2.text}")

if __name__ == "__main__":
    final_verify()
