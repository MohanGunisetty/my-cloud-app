from flask import Flask, render_template, request, redirect, url_for, session, jsonify, Response, stream_with_context
import os
import requests
import json
import time
from dotenv import load_dotenv
from chunker import read_in_chunks, CHUNK_SIZE
from auth import hash_password, verify_password_hash

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'default-dev-key-123')

# SECURITY WARNING: Hardcoded secrets for quick fix.
TELEGRAM_BOT_TOKEN = "8471088417:AAGjfOdUyRWVM7z4DrvZmY4YHmjq4duavVY"
TELEGRAM_STORAGE_CHANNEL_ID = "-1003842345696"
TELEGRAM_METADATA_CHANNEL_ID = "-1003742575415"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
TELEGRAM_FILE_URL = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}"

# IN-MEMORY DATABASES
FILES_DB = []
AUTH_DB = {}
# Upload Progress Cache: { 'user_email': 45 } (percentage)
UPLOAD_STATUS = {}

# --- HELPER: SMART RETRY LOGIC (PRIORITY 1) ---
def upload_chunk_with_retry(files, data, retries=3):
    for attempt in range(1, retries + 1):
        try:
            resp = requests.post(f"{TELEGRAM_API_URL}/sendDocument", data=data, files=files, timeout=300)
            if resp.status_code == 200 and resp.json().get('ok'):
                return resp.json()
            else:
                print(f"[ERROR] Telegram responded: {resp.status_code} {resp.text}")
                raise Exception(f"Telegram Error {resp.status_code}: {resp.text}")
        except Exception as e:
            print(f"[RETRY] Attempt {attempt} failed: {e}")
        time.sleep(attempt * 1) # Faster retry
    raise Exception("Telegram Upload Failed: Max retries exceeded")

# --- MIDDLEWARE ---
def is_authenticated():
    return session.get('authenticated') and session.get('user_id')

@app.route('/')
def home():
    if is_authenticated(): return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            session['pre_auth_email'] = email
            if email in AUTH_DB: return redirect(url_for('verify_password'))
            else: return redirect(url_for('create_password'))
    return render_template('login.html')

@app.route('/create-password', methods=['GET', 'POST'])
def create_password():
    email = session.get('pre_auth_email')
    if not email: return redirect(url_for('login'))
    if request.method == 'POST':
        password = request.form.get('password')
        if password:
            p_hash = hash_password(password)
            # Metadata logging disabled to prevent freeze
            pass
            AUTH_DB[email] = p_hash
            session['user_id'] = email
            session['authenticated'] = True
            return redirect(url_for('dashboard'))
    return render_template('create_password.html', email=email)

@app.route('/verify-password', methods=['GET', 'POST'])
def verify_password():
    email = session.get('pre_auth_email')
    if not email: return redirect(url_for('login'))
    error = None
    if request.method == 'POST':
        password = request.form.get('password')
        stored_hash = AUTH_DB.get(email)
        if stored_hash and verify_password_hash(password, stored_hash):
            session['user_id'] = email
            session['authenticated'] = True
            return redirect(url_for('dashboard'))
        else: error = "Incorrect password."
    return render_template('verify_password.html', email=email, error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- CORE STORAGE FEATURES ---

@app.route('/dashboard')
@app.route('/dashboard')
def dashboard():
    if not is_authenticated(): return redirect(url_for('login'))
    user_id = session['user_id']
    current_path = request.args.get('path', '/')
    
    # Filter files for current directory
    # 1. Files in this path
    # 2. Folders in this path
    files_in_dir = []
    for f in FILES_DB:
        if f.get('user') != user_id: continue
        f_path = f.get('path', '/')
        if f_path == current_path:
            files_in_dir.append(f)

    # Priority 3: Storage Stats (Total)
    all_user_files = [f for f in FILES_DB if f.get('user') == user_id and f.get('type', 'file') == 'file']
    total_usage = sum(f.get('size', 0) for f in all_user_files)
    
    # Breadcrumbs
    parts = [p for p in current_path.strip('/').split('/') if p]
    breadcrumbs = []
    accum = '/'
    for p in parts:
        accum += p + '/'
        breadcrumbs.append({'name': p, 'path': accum})

    return render_template('dashboard.html', user_id=user_id, files=files_in_dir, usage_bytes=total_usage, current_path=current_path, breadcrumbs=breadcrumbs)

@app.route('/upload_chunk', methods=['POST'])
def upload_chunk():
    if not is_authenticated(): return jsonify({'error': 'Unauthorized'}), 401
    
    if 'file' not in request.files: return jsonify({'error': 'No file'}), 400
    file_part = request.files['file']
    chunk_index = request.form.get('chunkIndex', '0')
    filename = request.form.get('filename', 'unknown')
    
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_STORAGE_CHANNEL_ID:
        return jsonify({'error': 'Server Config Error: Missing TELEGRAM_BOT_TOKEN or STORAGE_ID'}), 500
    
    try:
        # Read the chunk data directly from the upload stream
        chunk_data = file_part.read()
        
        # Prepare Telegram Payload
        files = {'document': (f"{filename}.p{chunk_index}", chunk_data)}
        data = {'chat_id': TELEGRAM_STORAGE_CHANNEL_ID, 'caption': f"Chunk {chunk_index} of {filename}"}
        
        # Upload to Telegram
        res = upload_chunk_with_retry(files, data)
        doc = res['result']['document']
        
        return jsonify({
            'status': 'success',
            'file_id': doc['file_id'],
            'size': doc.get('file_size', 0)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/upload_complete', methods=['POST'])
def upload_complete():
    if not is_authenticated(): return jsonify({'error': 'Unauthorized'}), 401
    user_id = session['user_id']
    
    data = request.json
    if not data: return jsonify({'error': 'No data'}), 400
    
    filename = data.get('filename')
    total_size = data.get('total_size')
    chunk_ids = data.get('chunk_ids')
    
    if not filename or not chunk_ids:
        return jsonify({'error': 'Invalid metadata'}), 400
        
    try:
        # Metadata logging disabled
        pass
        
        # Save to In-Memory DB
        FILES_DB.append({
            'name': filename,
            'user': user_id,
            'size': total_size,
            'total_chunks': len(chunk_ids),
            'chunk_ids': chunk_ids,
            'type': 'file',
            'path': data.get('path', '/')
        })
        
        return jsonify({'status': 'success'})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/create_folder', methods=['POST'])
def create_folder():
    if not is_authenticated(): return jsonify({'error': 'Unauthorized'}), 401
    user_id = session['user_id']
    folder_name = request.form.get('folder_name')
    current_path = request.form.get('path', '/')
    
    if not folder_name: return jsonify({'error': 'Name required'}), 400
    
    # Check if exists
    full_path = current_path + folder_name + '/'
    exists = any(f['path'] == full_path and f['user'] == user_id for f in FILES_DB)
    if exists: return jsonify({'error': 'Folder exists'}), 400
    
    FILES_DB.append({
        'name': folder_name,
        'user': user_id,
        'size': 0,
        'type': 'folder',
        'path': current_path
    })
    return redirect(url_for('dashboard', path=current_path))

@app.route('/download/<path:filename>')
def download(filename):
    if not is_authenticated(): return jsonify({'error': 'Unauthorized'}), 401
    file_record = next((f for f in FILES_DB if f['name'] == filename and f['user'] == session['user_id']), None)
    if not file_record: return "File not found", 404
    def generate():
        for fid in file_record['chunk_ids']:
            path_info = requests.get(f"{TELEGRAM_API_URL}/getFile", params={'file_id': fid}).json()
            if path_info.get('ok'):
                d_url = f"{TELEGRAM_FILE_URL}/{path_info['result']['file_path']}"
                with requests.get(d_url, stream=True) as r:
                    for c in r.iter_content(8192):
                        yield c
    return Response(stream_with_context(generate()), headers={
        "Content-Disposition": f"attachment; filename={filename}",
        "Content-Type": "application/octet-stream",
        "Content-Length": str(file_record['size'])
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
