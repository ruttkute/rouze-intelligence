"""
ROUZE SECURE FILE UPLOAD CONFIGURATION
Security-focused settings for client data handling
"""

import os
from datetime import timedelta

# File Upload Settings
UPLOAD_FOLDER = 'uploads/client_data'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'json', 'txt'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB max
MAX_TOTAL_UPLOADS_PER_CLIENT = 5

# Security Settings
ENCRYPTION_ENABLED = True
DELETE_AFTER_DAYS = 30  # Auto-delete files after 30 days
REQUIRE_GDPR_CONSENT = True
AUDIT_LOGGING = True

# File naming (anonymize uploaded files)
def secure_filename_generator(original_filename, client_id):
    """
    Generate secure filename that doesn't expose sensitive info
    
    Example: client_001_data_2025-11-19_abc123.csv
    (NOT: John_Smiths_Confidential_Sales.csv)
    """
    import hashlib
    import secrets
    
    # Get file extension
    file_ext = original_filename.split('.')[-1]
    
    # Generate random token
    random_token = secrets.token_hex(8)
    
    # Create anonymous filename
    safe_name = f"client_{client_id}_data_{random_token}.{file_ext}"
    
    return safe_name

# Validation Rules
FILE_VALIDATION_RULES = {
    'csv': {
        'max_rows': 100000,
        'allowed_columns': ['*'],  # Allow any columns (client responsible)
        'check': 'csv_structure'
    },
    'xlsx': {
        'max_rows': 50000,
        'max_sheets': 10,
        'check': 'excel_structure'
    },
    'json': {
        'max_size': 5 * 1024 * 1024,  # 5MB
        'check': 'json_valid'
    }
}

# Legal/Privacy Settings
GDPR_COMPLIANCE = {
    'require_consent': True,
    'consent_version': '1.0',
    'data_processor': 'Rouze Intelligence',
    'data_location': 'Secure server (encrypted)',
    'retention_period': '30 days'
}

