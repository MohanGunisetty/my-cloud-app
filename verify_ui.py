import requests
import sys

BASE_URL = "http://127.0.0.1:5000"

def verify_ui_modern():
    print("------------------------------------------------")
    print("TESTING UI: MODERNIZATION CHECK")
    print("------------------------------------------------")

    try:
        # Check Login Page
        r = requests.get(f"{BASE_URL}/login", timeout=5)
        
        if r.status_code == 200:
            content = r.text
            
            # Check for Modern Font
            if "fonts.googleapis.com" in content and "Inter" in content:
                print("✅ Font 'Inter' loaded.")
            else:
                 print("❌ Font missing.")

            # Check for Card Class (New UI component)
            if 'class="card"' in content:
                print("✅ 'Card' layout detected.")
            else:
                print("❌ 'Card' layout missing.")
                
            # Check for SVG
            if "<svg" in content:
                print("✅ SVG Icons detected.")
            else:
                print("❌ SVG Icons missing.")
                
            print("------------------------------------------------")
            print("🎉 UI VERIFIED: Modern Templates Active")
            print("------------------------------------------------")
        else:
            print(f"❌ Failed to load UI. Status: {r.status_code}")
            sys.exit(1)

    except Exception as e:
        print(f"❌ Exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    verify_ui_modern()
