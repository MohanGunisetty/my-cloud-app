import requests
import time
import sys

BASE_URL = "http://127.0.0.1:5000"

def check_login_robust():
    print("------------------------------------------------")
    print("TESTING STEP 5: LOGIN LOGIC")
    print("------------------------------------------------")
    
    # Session to keep cookies
    s = requests.Session()

    # 1. Wait for server to be up
    print("1. Checking Server Connectivity...")
    try:
        requests.get(BASE_URL, timeout=5)
    except:
        print("❌ Server NOT reachable. Is app.py running?")
        sys.exit(1)

    # 2. Access Login Page
    print("2. Fetching Login Page...")
    r1 = s.get(f"{BASE_URL}/login")
    if r1.status_code == 200:
        if "email" in r1.text.lower():
            print("✅ Login Page Loaded (Form detected)")
        else:
            print("❌ Login Page Loaded but FORM missing")
            print(f"Debug Snippet: {r1.text[:100]}")
            sys.exit(1)
    else:
        print(f"❌ Failed to load login page. Status: {r1.status_code}")
        sys.exit(1)

    # 3. Submit Form
    print("3. Submitting Login Form...")
    test_email = "verified_user@example.com"
    r2 = s.post(f"{BASE_URL}/login", data={'email': test_email}, allow_redirects=True)
    
    # 4. Check Result
    print(f"4. Verifying Redirect (Expected /dashboard, Got {r2.url})...")
    if "/dashboard" in r2.url:
        print("✅ Redirected to Dashboard successfully")
    else:
        print("❌ Did not redirect to dashboard.")
        sys.exit(1)

    # 5. Check Content
    print("5. Verifying User Identity in Dashboard...")
    if test_email in r2.text:
        print(f"✅ Identity Found: '{test_email}' is visible on page.")
        print("------------------------------------------------")
        print("🎉 STEP 5 COMPLETE & VERIFIED")
        print("------------------------------------------------")
    else:
        print("❌ Dashboard loaded, but email NOT found in text.")
        sys.exit(1)

if __name__ == "__main__":
    check_login_robust()
