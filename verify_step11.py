import requests
import sys
import os
import hashlib

BASE_URL = "http://127.0.0.1:5000"

def verify_step11():
    print("------------------------------------------------")
    print("TESTING STEP 11: DOWNLOAD & REBUILD")
    print("------------------------------------------------")

    s = requests.Session()
    
    # 1. Login
    print("1. Logging in...")
    try:
        s.post(f"{BASE_URL}/login", data={'email': 'down_tester@example.com'})
    except:
        print("❌ Server Down")
        sys.exit(1)

    # 2. Create & Upload Test File
    fname = "download_test.bin"
    original_content = os.urandom(1024 * 1024 * 2) # 2MB file (small enough but tests stream)
    original_hash = hashlib.md5(original_content).hexdigest()
    
    print(f"2. Creating 2MB test file (Hash: {original_hash})...")
    with open(fname, "wb") as f:
        f.write(original_content)

    print("3. Uploading file...")
    try:
        with open(fname, "rb") as f:
            r = s.post(f"{BASE_URL}/upload", files={'file': f})
        
        if r.status_code != 200 or r.json().get('status') != 'success':
            print(f"❌ Upload Failed: {r.text}")
            sys.exit(1)
        print("✅ Upload Success.")
    except Exception as e:
        print(f"❌ Exception during upload: {e}")
        sys.exit(1)

    # 3. Download & Verify
    print("4. Downloading file...")
    try:
        # Stream download
        download_r = s.get(f"{BASE_URL}/download/{fname}", stream=True)
        
        if download_r.status_code == 200:
            downloaded_content = b""
            for chunk in download_r.iter_content(chunk_size=8192):
                if chunk:
                    downloaded_content += chunk
            
            downloaded_hash = hashlib.md5(downloaded_content).hexdigest()
            print(f"   Downloaded size: {len(downloaded_content)} bytes")
            print(f"   Downloaded Hash: {downloaded_hash}")

            if downloaded_hash == original_hash:
                print("✅ Hashes Match! File Rebuilt Successfully.")
                print("------------------------------------------------")
                print("🎉 STEP 11 COMPLETE & VERIFIED")
                print("------------------------------------------------")
            else:
                print("❌ Hash Mismatch! Corruption occurred.")
                sys.exit(1)
        else:
             print(f"❌ Download Failed: {download_r.status_code} - {download_r.text}")
             sys.exit(1)

    except Exception as e:
        print(f"❌ Exception during download: {e}")
    
    # Cleanup
    if os.path.exists(fname):
        try: os.remove(fname)
        except: pass

if __name__ == "__main__":
    verify_step11()
