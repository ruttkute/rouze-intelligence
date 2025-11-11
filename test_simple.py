#!/usr/bin/env python3
"""ROUZE Healthcare System - Auto-Install Version"""

print("🔧 Step 1: Installing required packages...")
import subprocess
import sys

# Auto-install dependencies
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "python-dotenv", "anthropic"])
print("✅ Packages installed")

print("🔧 Step 2: Loading dotenv...")
from dotenv import load_dotenv
import os
load_dotenv()
print("✅ dotenv loaded")

print("🔧 Step 3: Checking API key...")
api_key = os.getenv('ANTHROPIC_API_KEY')
if api_key:
    print(f"✅ API key found: {api_key[:20]}...")
else:
    print("❌ No API key in .env file!")
    sys.exit(1)

print("🔧 Step 4: Connecting to Claude...")
import anthropic
client = anthropic.Anthropic(api_key=api_key)
print("✅ Claude client created")

print("🔧 Step 5: Testing API (10 seconds)...")
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=50,
    messages=[{"role": "user", "content": "Say hello from ROUZE!"}]
)
print(f"✅ Response: {message.content[0].text}")
print("\n🎉 SUCCESS! Everything works!")
print("\n💼 Ready to generate healthcare intelligence reports!")