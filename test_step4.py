import requests

BASE_URL = "http://127.0.0.1:5000"
s = requests.Session()

def check_step4():
    print("Checking Step 4 Routes...")
    
    # 1. Home -> Login Redirect
    r1 = s.get(BASE_URL)
    if r1.url.endswith('/login') and r1.status_code == 200:
        print("✅ Home -> Redirects to Login")
    else:
        print(f"❌ Home Redirect Failed. Got {r1.url}")
        return

    # 2. Check Login Page Content
    if "Welcome to MyCloud" in r1.text:
        print("✅ Login Page Loaded")
    else:
        print("❌ Login Page Content Missing")
        return

    # 3. Dev Login (Simulating Auth)
    r2 = s.get(f"{BASE_URL}/dev_login")
    if r2.url.endswith('/dashboard') and r2.status_code == 200:
        print("✅ Dev Login -> Redirects to Dashboard")
    else:
        print(f"❌ Dev Login Failed. Got {r2.url}")
        return

    # 4. Check Dashboard Content
    if "User: dev_user" in r2.text:
        print("✅ Dashboard Shows User ID")
    else:
        print("❌ Dashboard Content Missing")
        return

    # 5. Check Logout
    r3 = s.get(f"{BASE_URL}/logout")
    if r3.url.endswith('/login'):
        print("✅ Logout -> Redirects to Login")
    else:
        print("❌ Logout Failed")
        return

    print("\n🎉 STEP 4 PASSED: All routes functional.")

if __name__ == "__main__":
    try:
        check_step4()
    except Exception as e:
        print(f"❌ Connectivity Error: {e}")
        print("Is app.py running?")
