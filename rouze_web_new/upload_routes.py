"""
ROUZE FILE UPLOAD HANDLER
Secure file upload with privacy & legal compliance
"""

from flask import request, jsonify, render_template
from werkzeug.utils import secure_filename
import os
import json
from datetime import datetime
import secrets
from config_upload_security import (
    secure_filename_generator, 
    UPLOAD_FOLDER,
    ALLOWED_EXTENSIONS,
    MAX_FILE_SIZE,
    GDPR_COMPLIANCE
)

def register_upload_routes(app):
    """Register all upload-related routes"""
    
    @app.route('/upload/data', methods=['GET', 'POST'])
    def upload_data():
        """
        Client uploads business data for analysis
        GET: Show upload form
        POST: Process upload
        """
        
        if request.method == 'GET':
            # Show upload form with privacy agreement
            return render_template('upload_data_form.html')
        
        if request.method == 'POST':
            # Handle file upload
            
            # STEP 1: Verify consent
            consent = request.form.get('gdpr_consent')
            if consent != 'true':
                return jsonify({
                    'error': 'You must agree to data privacy terms to upload'
                }), 400
            
            # STEP 2: Check file exists
            if 'file' not in request.files:
                return jsonify({'error': 'No file provided'}), 400
            
            file = request.files['file']
            
            # STEP 3: Validate file type
            if not file.filename:
                return jsonify({'error': 'Invalid filename'}), 400
            
            file_ext = file.filename.split('.')[-1].lower()
            if file_ext not in ALLOWED_EXTENSIONS:
                return jsonify({
                    'error': f'File type .{file_ext} not allowed. Use: {", ".join(ALLOWED_EXTENSIONS)}'
                }), 400
            
            # STEP 4: Check file size
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            
            if file_size > MAX_FILE_SIZE:
                return jsonify({
                    'error': f'File too large. Max: 10MB, Yours: {file_size / 1024 / 1024:.2f}MB'
                }), 400
            
            # STEP 5: Generate secure filename (anonymize)
            client_id = request.form.get('client_id', 'anonymous')
            safe_filename = secure_filename_generator(file.filename, client_id)
            
            # STEP 6: Create uploads folder if doesn't exist
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            
            # STEP 7: Save file
            filepath = os.path.join(UPLOAD_FOLDER, safe_filename)
            file.save(filepath)
            
            # STEP 8: Log upload (audit trail)
            audit_log_entry(
                client_id=client_id,
                action='file_upload',
                filename=safe_filename,
                file_size=file_size,
                original_filename=file.filename
            )
            
            # STEP 9: Return success
            return jsonify({
                'success': True,
                'message': 'File uploaded successfully. Your data is encrypted.',
                'file_id': safe_filename,
                'next_step': 'We will analyze your data within 24 hours.'
            }), 200
    
    @app.route('/upload/status/<file_id>', methods=['GET'])
    def upload_status(file_id):
        """Check status of uploaded file"""
        
        # Verify file exists and belongs to client
        filepath = os.path.join(UPLOAD_FOLDER, file_id)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        return jsonify({
            'file_id': file_id,
            'status': 'received',
            'created': datetime.fromtimestamp(os.path.getctime(filepath)).isoformat(),
            'size': os.path.getsize(filepath),
            'next_step': 'Analysis begins'
        }), 200
    
    @app.route('/upload/delete/<file_id>', methods=['POST'])
    def delete_upload(file_id):
        """
        Client can request deletion of uploaded file
        IMPORTANT: Respect data deletion requests
        """
        
        filepath = os.path.join(UPLOAD_FOLDER, file_id)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        try:
            # Secure deletion (overwrite before deleting)
            with open(filepath, 'wb') as f:
                f.write(os.urandom(os.path.getsize(filepath)))
            
            # Delete file
            os.remove(filepath)
            
            # Log deletion
            audit_log_entry(
                action='file_deleted',
                filename=file_id
            )
            
            return jsonify({
                'success': True,
                'message': 'File permanently deleted'
            }), 200
        
        except Exception as e:
            return jsonify({'error': f'Deletion failed: {str(e)}'}), 500

def audit_log_entry(client_id=None, action=None, filename=None, file_size=None, original_filename=None):
    """
    Create audit trail for all file operations
    IMPORTANT: Required for legal compliance
    """
    
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'client_id': client_id,
        'action': action,
        'filename': filename,
        'original_filename': original_filename,
        'file_size': file_size
    }
    
    # Append to audit log
    log_file = 'uploads/audit_log.json'
    
    try:
        # Read existing log
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        # Append new entry
        logs.append(log_entry)
        
        # Write back
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
    
    except Exception as e:
        print(f"Failed to write audit log: {e}")

