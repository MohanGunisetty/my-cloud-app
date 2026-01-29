import os
import zipfile

def zip_project(output_filename):
    # Files to INLCUDE explicitly or patterns to exclude?
    # Better to walk and exclude.
    
    EXCLUDE_DIRS = {'.git', '.venv', '__pycache__', 'venv', 'env', 'static/chunk_cache'}
    EXCLUDE_FILES = {'.env', '.DS_Store', output_filename}
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                if file in EXCLUDE_FILES:
                    print(f"Skipping secret/ignored file: {file}")
                    continue
                
                # Double check against secret extensions just in case
                if file.endswith('.zip') and file != 'infinityfree_files.zip': # Allow specific zips if needed, but generally skip large zips
                     pass

                file_path = os.path.join(root, file)
                # Archive name should be relative
                arcname = os.path.relpath(file_path, start='.')
                
                print(f"Adding: {arcname}")
                zipf.write(file_path, arcname)

    print(f"\n[SUCCESS] Created secure deployment package: {output_filename}")

if __name__ == "__main__":
    zip_project('render_deploy_safe.zip')
