import requests

BASE_URL = "http://127.0.0.1:5000"
s = requests.Session()

def check_login():
    print("Checking Step 5 (Login)...")
    
    # 1. Open Login Page
    r1 = s.get(f"{BASE_URL}/login")
    if "Sign In" in r1.text and "Email Address" in r1.text:
        print("✅ Login Page UI Loaded")
    else:
        print("❌ Login Page UI Failed")
        return

    # 2. Submit Login Form
    test_email = "tester@example.com"
    r2 = s.post(f"{BASE_URL}/login", data={'email': test_email})
    
    # 3. Check Redirect to Dashboard
    if r2.url.endswith('/dashboard') and r2.status_code == 200:
        print("✅ Login Redirect Success")
    else:
        print(f"❌ Login Redirect Failed. Url: {r2.url}")
        return

    # 4. Verify Identity
    if test_email in r2.text:
        print(f"✅ Identity Verified: Found '{test_email}' in dashboard")
    else:
        print(f"❌ Identity Missing from Dashboard")

    print("\n🎉 STEP 5 PASSED: Session Management Works")

if __name__ == "__main__":
    check_login()
