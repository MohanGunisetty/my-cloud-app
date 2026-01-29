import requests
import os
import pprint
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
STORAGE_ID = os.getenv('TELEGRAM_STORAGE_CHANNEL_ID')
METADATA_ID = os.getenv('TELEGRAM_METADATA_CHANNEL_ID')

BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def test_channels():
    print("------------------------------------------------")
    print(f"DEBUG: Testing with Token: ...{TOKEN[-5:] if TOKEN else 'None'}")
    print(f"DEBUG: Storage ID: {STORAGE_ID}")
    print(f"DEBUG: Metadata ID: {METADATA_ID}")
    print("------------------------------------------------")

    # TEST 1: STORAGE (Send Document)
    print(f"1. Testing Storage Channel ({STORAGE_ID})...")
    try:
        files = {'document': ('test.txt', b'This is a test file for storage.')}
        resp1 = requests.post(f"{BASE_URL}/sendDocument", data={'chat_id': STORAGE_ID}, files=files)
        data1 = resp1.json()
        
        if data1.get('ok'):
            print("Storage Channel: UPLOAD SUCCEEDED")
        else:
            print("Storage Channel: UPLOAD FAILED")
            print(f"Error Code: {data1.get('error_code')}")
            print(f"Description: {data1.get('description')}")
    except Exception as e:
        print(f"Storage Channel: EXCEPTION - {e}")

    print("------------------------------------------------")

    # TEST 2: METADATA (Send Text)
    print(f"2. Testing Metadata Channel ({METADATA_ID})...")
    try:
        resp2 = requests.post(f"{BASE_URL}/sendMessage", json={'chat_id': METADATA_ID, 'text': 'Test metadata entry'})
        data2 = resp2.json()
        
        if data2.get('ok'):
            print("Metadata Channel: MESSAGE SUCCEEDED")
        else:
            print("Metadata Channel: MESSAGE FAILED")
            print(f"Error Code: {data2.get('error_code')}")
            print(f"Description: {data2.get('description')}")
    except Exception as e:
        print(f"Metadata Channel: EXCEPTION - {e}")

    print("------------------------------------------------")

if __name__ == "__main__":
    test_channels()
