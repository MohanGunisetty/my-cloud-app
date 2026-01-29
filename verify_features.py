import requests
import sys

BASE_URL = "http://127.0.0.1:5000"

def verify_progress_and_stats():
    print("------------------------------------------------")
    print("TESTING PRIORITY 2 & 3: Progress & Stats")
    print("------------------------------------------------")
    
    s = requests.Session()
    # Login
    s.post(f"{BASE_URL}/login", data={'email': 'stats_tester@test.com'})
    s.post(f"{BASE_URL}/create-password", data={'password': '1234'})
    
    # 1. Check Upload Status Endpoint (Should return 0 initially)
    print("1. Checking /upload_status endpoint...")
    r = s.get(f"{BASE_URL}/upload_status")
    if r.status_code == 200 and 'percent' in r.json():
        print(f"✅ Endpoint active (Percent: {r.json()['percent']}%)")
    else:
        print(f"❌ Endpoint failed: {r.text}")
        sys.exit(1)

    # 2. Check Dashboard for Usage Stats HTML
    print("2. Checking Dashboard for 'Storage Used' badge...")
    r = s.get(f"{BASE_URL}/dashboard")
    if "Storage Used" in r.text and "MB" in r.text:
         print("✅ Storage Usage Badge found in HTML.")
         print("------------------------------------------------")
         print("🎉 PRIORITY 2 & 3 COMPLETE")
         print("------------------------------------------------")
    else:
        print("❌ Usage Badge MISSING in HTML.")
        sys.exit(1)

if __name__ == "__main__":
    verify_progress_and_stats()
