import zipfile
import os

files_for_infinityfree = [
    'index.php',
    '.htaccess',
    'redirect_fallback.html'
]

with zipfile.ZipFile('infinityfree_files.zip', 'w') as zipf:
    for file in files_for_infinityfree:
        if os.path.exists(file):
            zipf.write(file)
            print(f"Added {file}")

print("Created infinityfree_files.zip")
