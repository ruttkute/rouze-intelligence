#!/usr/bin/env python3
"""
DIAGNOSTIC TOOL - Find the Real Problem
"""
import os
import sys

print("="*70)
print("🔍 ROUZE DIAGNOSTIC TOOL")
print("="*70)

# 1. Python Location
print("\n1️⃣ PYTHON INFORMATION:")
print(f"   Python executable: {sys.executable}")
print(f"   Python version: {sys.version}")
print(f"   Current directory: {os.getcwd()}")

# 2. Check if in virtual environment
print("\n2️⃣ VIRTUAL ENVIRONMENT:")
if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
    print("   ✅ Running inside virtual environment")
    print(f"   Venv location: {sys.prefix}")
else:
    print("   ⚠️  NOT in virtual environment (this might be the problem!)")

# 3. List all .env files
print("\n3️⃣ SEARCHING FOR .env FILES:")
for root, dirs, files in os.walk(os.path.expanduser("~/Desktop/rouze")):
    if '.env' in files:
        env_path = os.path.join(root, '.env')
        print(f"   📄 Found: {env_path}")
        # Try to read it
        try:
            with open(env_path, 'r') as f:
                content = f.read()
                if 'ANTHROPIC_API_KEY' in content:
                    # Extract just the key part
                    for line in content.split('\n'):
                        if 'ANTHROPIC_API_KEY' in line:
                            parts = line.split('=')
                            if len(parts) > 1:
                                key_preview = parts[1].strip()[:20]
                                print(f"      Key preview: {key_preview}...")
                                print(f"      Key length: {len(parts[1].strip())} chars")
                                # Check for issues
                                if parts[1].strip().startswith('"') or parts[1].strip().startswith("'"):
                                    print("      ⚠️  WARNING: Key has quotes (remove them!)")
                                if ' ' in parts[1].strip():
                                    print("      ⚠️  WARNING: Key has spaces (remove them!)")
                else:
                    print("      ❌ No ANTHROPIC_API_KEY found in file")
        except Exception as e:
            print(f"      ❌ Cannot read: {e}")

# 4. Check dotenv package
print("\n4️⃣ CHECKING PACKAGES:")
try:
    import dotenv
    print(f"   ✅ python-dotenv installed: {dotenv.__file__}")
except ImportError:
    print("   ❌ python-dotenv NOT installed")

try:
    import anthropic
    print(f"   ✅ anthropic installed: {anthropic.__file__}")
except ImportError:
    print("   ❌ anthropic NOT installed")

# 5. Test loading .env
print("\n5️⃣ TESTING .env LOADING:")
try:
    from dotenv import load_dotenv
    
    # Try loading from current directory
    result = load_dotenv()
    print(f"   load_dotenv() returned: {result}")
    
    # Check what was loaded
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if api_key:
        print(f"   ✅ API key loaded: {api_key[:20]}... ({len(api_key)} chars)")
    else:
        print("   ❌ ANTHROPIC_API_KEY not in environment")
        
        # Try explicit paths
        print("\n   Trying explicit paths:")
        possible_paths = [
            '.env',
            '../.env',
            '../../.env',
            os.path.expanduser('~/Desktop/rouze/rouze_agent/.env'),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"   📄 Trying: {path}")
                load_dotenv(path)
                api_key = os.getenv('ANTHROPIC_API_KEY')
                if api_key:
                    print(f"      ✅ SUCCESS! Key loaded: {api_key[:20]}...")
                    break
                
except Exception as e:
    print(f"   ❌ Error: {e}")

# 6. Final diagnosis
print("\n"+"="*70)
print("📋 DIAGNOSIS COMPLETE")
print("="*70)

if not (hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)):
    print("🔴 PROBLEM: Not using virtual environment")
    print("   FIX: Run 'source venv/bin/activate' first")

try:
    from dotenv import load_dotenv
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("🔴 PROBLEM: API key not loading")
        print("   FIX: .env file might be in wrong location")
except:
    print("🔴 PROBLEM: Missing packages")
    print("   FIX: Run 'pip install python-dotenv anthropic'")

print("\nCopy this entire output and show it to me!")