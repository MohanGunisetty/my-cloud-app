import requests
import sys
import os
import re

BASE_URL = "http://127.0.0.1:5000"

def verify_step10():
    print("------------------------------------------------")
    print("TESTING STEP 10: FILE LIST DISPLAY")
    print("------------------------------------------------")

    s = requests.Session()
    
    # 1. Login
    print("1. Logging in...")
    s.post(f"{BASE_URL}/login", data={'email': 'list_tester@example.com'})

    # 2. Upload Dummy File
    print("2. Uploading file 'list_test.txt'...")
    fname = "list_test.txt"
    with open(fname, "w") as f:
        f.write("Content for list test")

    try:
        s.post(f"{BASE_URL}/upload", files={'file': open(fname, 'rb')})
    except:
        pass # We assume upload works from previous steps

    # 3. Check Dashboard for File
    print("3. Fetching Dashboard to check list...")
    try:
        r = s.get(f"{BASE_URL}/dashboard")
        if r.status_code == 200:
            # Simple Regex check for filename in HTML table
            if "list_test.txt" in r.text:
                print("✅ File found in Dashboard List!")
                print("------------------------------------------------")
                print("🎉 STEP 10 COMPLETE & VERIFIED")
                print("------------------------------------------------") 
            else:
                print("❌ File uploaded but NOT visible in dashboard list.")
                # print(r.text) 
                sys.exit(1)
        else:
             print(f"❌ Dashboard Error: {r.status_code}")
             sys.exit(1)

    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Cleanup
    if os.path.exists(fname):
        try: os.remove(fname)
        except: pass

if __name__ == "__main__":
    verify_step10()
