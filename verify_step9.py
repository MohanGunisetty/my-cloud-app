import requests
import sys
import os

BASE_URL = "http://127.0.0.1:5000"

def verify_step9():
    print("------------------------------------------------")
    print("TESTING STEP 9: METADATA STORAGE")
    print("------------------------------------------------")

    s = requests.Session()
    
    # 1. Login
    print("1. Logging in...")
    try:
        s.post(f"{BASE_URL}/login", data={'email': 'meta_tester@example.com'})
    except:
        print("❌ Server Down")
        sys.exit(1)

    # 2. Upload Small File
    print("2. Uploading file to trigger metadata...")
    fname = "meta_test.txt"
    with open(fname, "w") as f:
        f.write("Metadata Test Content")

    try:
        files = {'file': open(fname, 'rb')}
        r = s.post(f"{BASE_URL}/upload", files=files)
        
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
    
    # Cleanup
    if os.path.exists(fname):
        os.remove(fname)

if __name__ == "__main__":
    verify_step9()
