"""
ROUZE Intelligence API - Professional Edition
Clean architecture with separated HTML templates
"""

from flask import Flask, request, jsonify, send_file
from datetime import datetime
import json

app = Flask(__name__)

# API Keys storage
API_KEYS = {
    'demo_key_123': {
        'email': 'demo@example.com',
        'tier': 'professional',
        'created': '2025-10-12',
        'calls_used': 0,
        'calls_limit': 5000
    }
}

# Pricing tiers
TIERS = {
    'free': {'price': 0, 'calls_per_month': 100},
    'starter': {'price': 49, 'calls_per_month': 1000},
    'professional': {'price': 149, 'calls_per_month': 5000},
    'enterprise': {'price': 499, 'calls_per_month': 50000}
}

@app.route('/')
def landing_page():
    """Serve animated landing page"""
    return send_file('templates/landing.html')

@app.route('/docs')
def docs():
    """Serve documentation page"""
    return send_file('templates/docs.html')

@app.route('/api/v1/analyze', methods=['POST'])
def analyze():
    """Main analysis endpoint"""
    api_key = request.headers.get('X-API-Key')
    
    if not api_key or api_key not in API_KEYS:
        return jsonify({'error': 'Invalid API key'}), 401
    
    user = API_KEYS[api_key]
    
    if user['calls_used'] >= user['calls_limit']:
        return jsonify({
            'error': 'Monthly limit exceeded',
            'limit': user['calls_limit'],
            'used': user['calls_used']
        }), 429
    
    data = request.get_json()
    signals = data.get('signals', [])
    
    if not signals:
        return jsonify({'error': 'No signals provided'}), 400
    
    # Simple analysis (replace with real Rouze analyzer)
    analysis = {
        'sentiment': 'negative' if any('severe' in str(s).lower() for s in signals) else 'positive',
        'risk_score': len([s for s in signals if 'severe' in s.get('text', '').lower()]) * 30,
        'keywords': list(set([w for s in signals for w in s.get('text', '').split() if len(w) > 3]))[:5]
    }
    
    user['calls_used'] += 1
    
    return jsonify({
        'status': 'success',
        'input_count': len(signals),
        'analysis': analysis,
        'usage': {
            'calls_used': user['calls_used'],
            'calls_remaining': user['calls_limit'] - user['calls_used']
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/v1/usage', methods=['GET'])
def check_usage():
    """Check API usage"""
    api_key = request.headers.get('X-API-Key')
    
    if not api_key or api_key not in API_KEYS:
        return jsonify({'error': 'Invalid API key'}), 401
    
    user = API_KEYS[api_key]
    
    return jsonify({
        'tier': user['tier'],
        'calls_used': user['calls_used'],
        'calls_limit': user['calls_limit'],
        'calls_remaining': user['calls_limit'] - user['calls_used'],
        'reset_date': '2025-11-01'
    })

@app.route('/signup')
def signup():
    """Signup page"""
    tier = request.args.get('tier', 'free')
    tier_info = TIERS.get(tier, TIERS['free'])
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Sign Up - Rouze API</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            max-width: 600px;
            margin: 100px auto;
            text-align: center;
            padding: 40px;
            background: #000;
            color: #f8f6f0;
        }}
        .signup-box {{
            background: #1a1a1a;
            padding: 60px 40px;
            border-radius: 16px;
            border: 2px solid #a855f7;
            box-shadow: 0 0 40px rgba(168,85,247,0.3);
        }}
        h1 {{
            color: #a855f7;
            margin-bottom: 20px;
        }}
        .price {{
            font-size: 52px;
            font-weight: 700;
            background: linear-gradient(135deg, #a855f7 0%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 20px 0;
        }}
        .demo-notice {{
            background: #0a0a0a;
            padding: 25px;
            border-radius: 8px;
            margin: 30px 0;
            border-left: 4px solid #a855f7;
        }}
        code {{
            background: #1a1a1a;
            color: #a855f7;
            padding: 5px 10px;
            border-radius: 4px;
            font-family: monospace;
        }}
        a {{
            display: inline-block;
            background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
            color: white;
            padding: 15px 40px;
            text-decoration: none;
            border-radius: 8px;
            margin-top: 20px;
            font-weight: 600;
            transition: all 0.3s;
        }}
        a:hover {{
            transform: translateY(-2px);
            box-shadow: 0 0 30px rgba(168,85,247,0.6);
        }}
    </style>
</head>
<body>
    <div class="signup-box">
        <h1>Sign Up for {tier.title()} Plan</h1>
        <div class="price">${tier_info['price']}<span style="font-size:20px;color:#a8a8a8;">/mo</span></div>
        <p style="margin:25px 0;color:#d4d4d4;font-size:18px;">
            {tier_info['calls_per_month']:,} API calls per month
        </p>
        <div class="demo-notice">
            <strong style="color:#a855f7;">Demo Mode</strong><br>
            <p style="margin:15px 0;color:#a8a8a8;">
                In production, this integrates with Stripe for instant API key delivery.
            </p>
            <p style="margin-top:15px;">
                For now, use demo key: <code>demo_key_123</code>
            </p>
        </div>
        <a href="/">← Back to Home</a>
    </div>
</body>
</html>"""
    
    return html

if __name__ == '__main__':
    print("=" * 80)
    print("🌙 ROUZE INTELLIGENCE API - PROFESSIONAL EDITION")
    print("=" * 80)
    print()
    print("✨ FEATURES:")
    print("   • Purple neon glow aesthetic")
    print("   • Smooth scroll animations")
    print("   • Clean separated architecture")
    print("   • Professional animations")
    print()
    print("📍 Landing Page:    http://localhost:8000")
    print("📍 Documentation:   http://localhost:8000/docs")
    print("📍 API Endpoint:    http://localhost:8000/api/v1/analyze")
    print()
    print("🔑 Demo API Key:    demo_key_123")
    print()
    print("=" * 80)
    print()
    
    app.run(host='0.0.0.0', port=8000, debug=True)