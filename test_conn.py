import requests
try:
    response = requests.get('https://api.telegram.org', timeout=10)
    print(f"Telegram Status: {response.status_code}")
except Exception as e:
    print(f"Error: {e}")
