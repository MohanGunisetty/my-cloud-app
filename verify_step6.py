import requests
import sys

BASE_URL = "http://127.0.0.1:5000"

def verify_step6():
    print("------------------------------------------------")
    print("TESTING STEP 6: FILE UPLOAD")
    print("------------------------------------------------")

    s = requests.Session()

    # 1. Login first
    print("1. Logging in...")
    s.post(f"{BASE_URL}/login", data={'email': 'uploader@test.com'})

    # 2. Create a dummy small file
    print("2. Creating test file...")
    with open("small_test.txt", "w") as f:
        f.write("This is a small file content for Telegram Cloud.")

    # 3. Upload File
    print("3. Uploading file to /upload...")
    files = {'file': open('small_test.txt', 'rb')}
    
    try:
        r = s.post(f"{BASE_URL}/upload", files=files)
        
        if r.status_code == 200:
            data = r.json()
            if data.get('status') == 'success' and 'file_id' in data:
                print(f"✅ Success! File ID obtained: {data['file_id']}")
                print(f"   File Name: {data['file_name']}")
                print("------------------------------------------------")
                print("🎉 STEP 6 COMPLETE & VERIFIED")
                print("------------------------------------------------")
            else:
                print(f"❌ Upload returned 200 but failed content: {data}")
                sys.exit(1)
        else:
            print(f"❌ Upload Failed. Status: {r.status_code}")
            print(f"   Response: {r.text}")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify_step6()
