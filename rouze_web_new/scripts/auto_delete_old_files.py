#!/usr/bin/env python3
import os, json
from datetime import datetime, timedelta

UPLOAD_FOLDER = os.path.expanduser('~/Desktop/rouze/rouze_web_new/uploads/client_data')
AUDIT_LOG = os.path.expanduser('~/Desktop/rouze/rouze_web_new/uploads/audit_log.json')
RETENTION_DAYS = 30

def delete_old_files():
    now = datetime.now()
    cutoff_date = now - timedelta(days=RETENTION_DAYS)
    deleted_count = 0
    
    if not os.path.exists(UPLOAD_FOLDER):
        print(f"[{now.isoformat()}] Upload folder doesn't exist yet")
        return
    
    try:
        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if not os.path.isfile(filepath):
                continue
            file_time = datetime.fromtimestamp(os.path.getctime(filepath))
            if file_time < cutoff_date:
                try:
                    file_size = os.path.getsize(filepath)
                    with open(filepath, 'wb') as f:
                        f.write(os.urandom(file_size))
                    os.remove(filepath)
                    log_deletion(filename, file_time)
                    deleted_count += 1
                except Exception as e:
                    print(f"Delete failed: {e}")
        print(f"[{now.isoformat()}] Deleted {deleted_count} old files")
    except Exception as e:
        print(f"Error: {e}")

def log_deletion(filename, file_time):
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'action': 'auto_delete_old_file',
        'filename': filename,
        'file_created': file_time.isoformat()
    }
    try:
        if os.path.exists(AUDIT_LOG):
            with open(AUDIT_LOG, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        logs.append(log_entry)
        with open(AUDIT_LOG, 'w') as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        print(f"Log error: {e}")

if __name__ == '__main__':
    delete_old_files()
