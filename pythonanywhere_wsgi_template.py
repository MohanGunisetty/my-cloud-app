import sys
import os
from dotenv import load_dotenv

# -------------------------------------------------------------------------
# INSTRUCTIONS:
# 1. Go to the "Web" tab in PythonAnywhere.
# 2. Scroll down to "WSGI configuration file" and click the link (e.g., /var/www/...)
# 3. DELETE everything in that file.
# 4. PASTE the code below.
# 5. CHANGE 'YOUR_USERNAME_HERE' to your actual PythonAnywhere username below.
# -------------------------------------------------------------------------

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME_HERE'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Load environment variables
load_dotenv(os.path.join(project_home, '.env'))

# Import flask app but need to call it "application" for WSGI
from app import app as application
