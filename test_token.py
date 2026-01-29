import requests

TOKEN = "8471088417:AAGjfOdUyRWVM7z4DrvZmY4YHmjq4duavVY"
URL = f"https://api.telegram.org/bot{TOKEN}/getMe"

print(f"Testing Token: {TOKEN}")
try:
    resp = requests.get(URL)
    data = resp.json()
    
    if data.get("ok"):
        print("\n✅ SUCCESS! Token is valid.")
        print(f"Bot Name: {data['result']['first_name']}")
        print(f"Bot Username: @{data['result']['username']}")
    else:
        print("\n❌ FAILURE! Token rejected.")
        print(f"Error Code: {data.get('error_code')}")
        print(f"Description: {data.get('description')}")

except Exception as e:
    print(f"\n❌ CONNECTION ERROR: {e}")
