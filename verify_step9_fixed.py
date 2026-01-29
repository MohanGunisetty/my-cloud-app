import requests
import sys
import os
import time

BASE_URL = "http://127.0.0.1:5000"

def verify_step9_fixed():
    print("------------------------------------------------")
    print("TESTING STEP 9: METADATA STORAGE (Fixed)")
    print("------------------------------------------------")

    s = requests.Session()
    
    # 1. Login
    print("1. Logging in...")
    try:
        s.post(f"{BASE_URL}/login", data={'email': 'meta_tester@example.com'})
    except Exception as e:
        print(f"❌ Server Down: {e}")
        sys.exit(1)

    # 2. Upload Small File
    print("2. Uploading file to trigger metadata...")
    fname = "meta_test_fix.txt"
    try:
        with open(fname, "w") as f:
            f.write("Metadata Test Content")
    except:
        pass

    try:
        with open(fname, "rb") as f:
            files = {'file': f}
            r = s.post(f"{BASE_URL}/upload", files=files, timeout=30)
        
        if r.status_code == 200:
            data = r.json()
            if data.get('status') == 'success' and data.get('metadata_stored'):
                print(f"✅ Upload & Metadata Success!")
                print("------------------------------------------------")
                print("🎉 STEP 9 COMPLETE & VERIFIED")
                print("------------------------------------------------")
            else:
                print(f"❌ Application logic failed: {data}")
        else:
             print(f"❌ Upload HTTP Error: {r.status_code} - {r.text}")

    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Cleanup (Safe)
    try:
        if os.path.exists(fname):
            os.remove(fname)
    except:
        print("(Note: Cleanup failed, ignoring)")

if __name__ == "__main__":
    verify_step9_fixed()
