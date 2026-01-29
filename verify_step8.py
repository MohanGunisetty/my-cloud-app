import requests
import sys
import os

BASE_URL = "http://127.0.0.1:5000"

def verify_step8():
    print("------------------------------------------------")
    print("TESTING STEP 8: CHUNKED UPLOAD")
    print("------------------------------------------------")

    s = requests.Session()
    
    # 1. Login
    print("1. Logging in...")
    s.post(f"{BASE_URL}/login", data={'email': 'chunk_tester@example.com'})

    # 2. Create Dummy Large File (Simulated)
    # We will create a file slightly larger than chunk size to force split
    # For speed, we just use a small limit. 
    # BUT, the server logic is hardcoded to 49MB (as per prompt).
    # Trying to upload a 50MB file over localhost might be slow but let's try a smaller proof.
    # We will rely on unit tests for the 49MB cut, but here we test the LOOP logic.
    # To test the LOOP, we need > 49MB. That sucks for a quick test.
    # Alternative: We can execute the test with a smaller chunk size injection, but we can't easily change server code from here.
    
    # Let's create a 50MB file. It's not that big.
    print("2. Creating 50MB dummy file for 2-chunk test...")
    fname = "large_test_50MB.bin"
    with open(fname, "wb") as f:
        f.write(b"A" * (50 * 1024 * 1024))
    
    print("3. Uploading 50MB file (EXPECT LONG WAIT)...")
    try:
        files = {'file': open(fname, 'rb')}
        r = s.post(f"{BASE_URL}/upload", files=files, timeout=300) # 5 min timeout
        
        if r.status_code == 200:
            data = r.json()
            if data['status'] == 'success':
                print(f"✅ Upload Success!")
                print(f"   Total Chunks: {data['total_chunks']}")
                print(f"   Chunk IDs: {data['chunk_ids']}")
                
                if data['total_chunks'] >= 2:
                     print("✅ File was split into multiple chunks correctly.")
                     print("------------------------------------------------")
                     print("🎉 STEP 8 COMPLETE & VERIFIED")
                     print("------------------------------------------------")
                else:
                    print("❌ Warning: File was NOT split. Did you set 49MB limit?")
            else:
                print(f"❌ Upload Failed (Logic Error): {data}")
        else:
             print(f"❌ Upload HTTP Error: {r.status_code} - {r.text}")

    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Cleanup
    if os.path.exists(fname):
        os.remove(fname)

if __name__ == "__main__":
    verify_step8()
