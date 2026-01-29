import requests
import os
import pprint
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"

def get_channel_ids():
    print("------------------------------------------------")
    print("DEBUG: Fetching updates...")
    try:
        # Get updates with allowed_updates to ensure we see everything
        resp = requests.get(f"{BASE_URL}/getUpdates", params={"allowed_updates": ["channel_post", "my_chat_member", "message"]})
        data = resp.json()
        
        if not data.get('ok'):
            print(f"Error response: {data}")
            return

        results = data.get('result', [])
        print(f"DEBUG: Found {len(results)} updates.")
        
        found = False
        for update in results:
            # pprint.pprint(update) # Too noisy, inspect keys
            
            chat_id = None
            title = None
            type_ = "unknown"

            if 'channel_post' in update:
                chat = update['channel_post']['chat']
                chat_id = chat['id']
                title = chat.get('title')
                type_ = "channel_post"
            
            elif 'my_chat_member' in update:
                chat = update['my_chat_member']['chat']
                chat_id = chat['id']
                title = chat.get('title')
                type_ = "bot_added_to_channel"
                
            elif 'message' in update:
                # Check if it's a forwarded message from a channel
                if 'forward_from_chat' in update['message']:
                    chat = update['message']['forward_from_chat']
                    chat_id = chat['id']
                    title = chat.get('title')
                    type_ = "forwarded_from_channel"
            
            if chat_id:
                print(f"✅ FOUND CHANNEL: {title} (ID: {chat_id}) [Source: {type_}]")
                found = True

        if not found:
            print("❌ No channel info found in updates.")
            print("Please FORWARD a message from your channel to the bot @Telestore80bot")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_channel_ids()
