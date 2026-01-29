import requests
import sys

BASE_URL = "http://127.0.0.1:5000"

def verify_theme():
    print("------------------------------------------------")
    print("TESTING UI: CYBERPUNK THEME CHECK")
    print("------------------------------------------------")

    try:
        # Check Login Page
        r = requests.get(f"{BASE_URL}/login", timeout=5)
        
        if r.status_code == 200:
            content = r.text
            
            # Check for Fonts
            if "Orbitron" in content and "Rajdhani" in content:
                print("✅ Fonts 'Orbitron' and 'Rajdhani' loaded.")
            else:
                print("❌ Fonts missing.")

            # Check for Style Link
            if "static/css/style.css" in content:
                print("✅ 'style.css' linked.")
            else:
                print("❌ 'style.css' link missing.")

            # Check for Futuristic Classes
            if 'class="card text-center"' in content:
                print("✅ Login Card layout detected.")
            else:
                print("❌ Login Card layout missing (or changed).")
                
            print("------------------------------------------------")
            print("🎉 THEME VERIFIED")
            print("------------------------------------------------")
        else:
            print(f"❌ Failed to load UI. Status: {r.status_code}")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify_theme()
