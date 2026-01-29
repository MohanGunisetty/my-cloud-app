import zipfile
import os

files_to_zip = [
    'app.py',
    'auth.py',
    'chunker.py',
    'requirements.txt',
    'Procfile',
    '.gitignore',
    '.env',
    'pythonanywhere_wsgi_template.py'
]

folders_to_zip = [
    'templates',
    'static'
]

with zipfile.ZipFile('project_deploy.zip', 'w') as zipf:
    for file in files_to_zip:
        if os.path.exists(file):
            zipf.write(file)
            print(f"Added {file}")
    
    for folder in folders_to_zip:
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path)
                print(f"Added {file_path}")

print("Created project_deploy.zip")
