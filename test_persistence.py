import requests
import json
import time

TELEGRAM_BOT_TOKEN = "8471088417:AAGjfOdUyRWVM7z4DrvZmY4YHmjq4duavVY"
TELEGRAM_METADATA_CHANNEL_ID = "-1003742575415"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
TELEGRAM_FILE_URL = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}"

print(f"Testing Persistence on Channel: {TELEGRAM_METADATA_CHANNEL_ID}")

# 1. TEST SAVE (Upload & Pin)
print("\n[1] Testing SAVE...")
try:
    db_state = {'test': 'data', 'timestamp': time.time()}
    files = {'document': ('db_test.json', json.dumps(db_state))}
    
    # Send
    res = requests.post(f"{TELEGRAM_API_URL}/sendDocument", data={'chat_id': TELEGRAM_METADATA_CHANNEL_ID, 'caption': 'TEST_BACKUP'}, files=files).json()
    
    if not res.get('ok'):
        print(f"❌ Upload Failed: {res}")
        exit()
        
    msg_id = res['result']['message_id']
    print(f"✅ Upload Success! Msg ID: {msg_id}")
    
    # Pin
    pin_res = requests.post(f"{TELEGRAM_API_URL}/pinChatMessage", data={'chat_id': TELEGRAM_METADATA_CHANNEL_ID, 'message_id': msg_id}).json()
    if pin_res.get('ok'):
        print("✅ Pin Success!")
    else:
        print(f"❌ Pin Failed: {pin_res}")
        
except Exception as e:
    print(f"❌ Save Error: {e}")
    exit()

# 2. TEST LOAD (Get Chat -> Pinned -> File)
print("\n[2] Testing LOAD...")
try:
    chat = requests.get(f"{TELEGRAM_API_URL}/getChat", params={'chat_id': TELEGRAM_METADATA_CHANNEL_ID}).json()
    if not chat.get('ok'):
        print(f"❌ GetChat Failed: {chat}")
        exit()
        
    pinned = chat['result'].get('pinned_message')
    if not pinned:
        print("❌ No Pinned Message found!")
        exit()
        
    doc = pinned.get('document')
    if not doc:
        print("❌ Pinned message has no document!")
        exit()
        
    print(f"Found Pinned Document: {doc['file_name']}")
    
    # Get File Path
    f_res = requests.get(f"{TELEGRAM_API_URL}/getFile", params={'file_id': doc['file_id']}).json()
    if not f_res.get('ok'):
        print(f"❌ GetFile Failed: {f_res}")
        exit()
        
    # Download content
    file_path = f_res['result']['file_path']
    content_res = requests.get(f"{TELEGRAM_FILE_URL}/{file_path}")
    
    if content_res.status_code == 200:
        data = content_res.json()
        print(f"✅ Download Success! Content: {data}")
    else:
        print(f"❌ Download Failed: {content_res.status_code}")

except Exception as e:
    print(f"❌ Load Error: {e}")
