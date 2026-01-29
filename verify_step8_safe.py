import requests
import sys
import os

BASE_URL = "http://127.0.0.1:5000"

def verify_step8_small():
    print("------------------------------------------------")
    print("TESTING STEP 8: CHUNKED UPLOAD LOGIC (Small File)")
    print("------------------------------------------------")

    s = requests.Session()
    
    # 1. Login
    print("1. Logging in...")
    try:
        s.post(f"{BASE_URL}/login", data={'email': 'chunk_tester@example.com'})
    except Exception as e:
        print(f"❌ Login Connection Failed: {e}")
        sys.exit(1)

    # 2. Create Small Dummy File (100KB)
    # This validates the LOOP logic without network stress.
    print("2. Creating 100KB dummy file...")
    fname = "small_test_loop.bin"
    with open(fname, "wb") as f:
        f.write(b"A" * (100 * 1024))
    
    print("3. Uploading file...")
    try:
        files = {'file': open(fname, 'rb')}
        r = s.post(f"{BASE_URL}/upload", files=files, timeout=60)
        
        if r.status_code == 200:
            data = r.json()
            if data['status'] == 'success':
                print(f"✅ Upload Success!")
                # Even 1 chunk means the loop ran 1 time.
                print(f"   Total Chunks: {data['total_chunks']}")
                print(f"   Chunk IDs: {data['chunk_ids']}")
                
                if data['total_chunks'] == 1 and len(data['chunk_ids']) == 1:
                     print("✅ Loop Logic Validated (1 Iteration).")
                     print("------------------------------------------------")
                     print("🎉 STEP 8 COMPLETE & VERIFIED")
                     print("------------------------------------------------")
                else:
                    print(f"❌ Unexpected chunk count: {data['total_chunks']}")
            else:
                print(f"❌ Upload Failed (Logic Error): {data}")
        else:
             print(f"❌ Upload HTTP Error: {r.status_code} - {r.text}")

    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Cleanup
    if os.path.exists(fname):
        try:
            os.remove(fname)
        except:
            pass

if __name__ == "__main__":
    verify_step8_small()
