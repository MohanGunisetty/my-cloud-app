import requests
import sys

BASE_URL = "http://127.0.0.1:5000"

def verify_security_flow():
    print("------------------------------------------------")
    print("TESTING SECURITY: AUTH & PASSWORD LAYER")
    print("------------------------------------------------")
    
    s = requests.Session()
    
    # 1. Access Dashboard Direct (Should Fail/Redirect)
    print("1. Attempting Direct Access to /dashboard...")
    r = s.get(f"{BASE_URL}/dashboard")
    if r.url == f"{BASE_URL}/login":
        print("✅ Access Denied: Redirected to Login.")
    else:
        print(f"❌ Failed: Accessed {r.url} without auth.")
        sys.exit(1)

    # 2. Login as New User (Should Redirect to Create Password)
    print("2. Logging in as 'new_sec_user'...")
    r = s.post(f"{BASE_URL}/login", data={'email': 'new_sec_user@test.com'})
    
    if "/create-password" in r.url:
        print("✅ Detected New User -> Redirected to Create Password.")
    else:
        print(f"❌ Failed: Redirected to {r.url} instead of Create Password.")
        sys.exit(1)

    # 3. Set Password (Should Redirect to Dashboard)
    print("3. Creating Password 'my_secret_123'...")
    r = s.post(f"{BASE_URL}/create-password", data={'password': 'my_secret_123'})
    
    if "/dashboard" in r.url:
        print("✅ Password Set & Logged In (Dashboard Access).")
    else:
         print(f"❌ Failed: Could not set password. Url: {r.url}")
         sys.exit(1)
         
    # 4. Logout (Should Clear Session)
    print("4. Logging Out...")
    s.get(f"{BASE_URL}/logout")
    
    # 5. Login Again (Should Redirect to Verify Password)
    print("5. Logging in Again (Existing User)...")
    r = s.post(f"{BASE_URL}/login", data={'email': 'new_sec_user@test.com'})
    
    if "/verify-password" in r.url:
        print("✅ Detected Existing User -> Redirected to Verify Password.")
    else:
         print(f"❌ Failed: Redirected to {r.url} instead of Verify Password.")
         sys.exit(1)

    # 6. Enter Wrong Password
    print("6. Entering Wrong Password...")
    r = s.post(f"{BASE_URL}/verify-password", data={'password': 'wrong_pass'})
    if "Incorrect password" in r.text or "/verify-password" in r.url:
        print("✅ Access Denied for Wrong Password.")
    else:
         print("❌ Failed: Wrong password accepted!")
         sys.exit(1)

    # 7. Enter Correct Password
    print("7. Entering Correct Password...")
    r = s.post(f"{BASE_URL}/verify-password", data={'password': 'my_secret_123'})
    if "/dashboard" in r.url:
        print("✅ Password Verified -> Access Granted.")
        print("------------------------------------------------")
        print("🎉 SECURITY LAYER VERIFIED")
        print("------------------------------------------------")
    else:
         print(f"❌ Failed to verify correct password. Url: {r.url}")
         sys.exit(1)

if __name__ == "__main__":
    verify_security_flow()
