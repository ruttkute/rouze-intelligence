from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'rouze_production_key_2025')

# Landing page
@app.route('/')
def index():
    return render_template('index.html')

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# Methodology page
@app.route('/methodology')
def methodology():
    return render_template('methodology.html')

# Services overview
@app.route('/services')
def services():
    return render_template('services.html')

# Industry-specific intake forms
@app.route('/intake/healthcare')
def intake_healthcare():
    return render_template('intake_healthcare.html')

@app.route('/intake/saas')
def intake_saas():
    return render_template('intake_saas.html')

@app.route('/intake/ecommerce')
def intake_ecommerce():
    return render_template('intake_ecommerce.html')

# Pricing pages
@app.route('/pricing/<industry>')
def pricing(industry):
    return render_template(f'pricing_{industry}.html', industry=industry)

# API endpoints
@app.route('/api/submit-intake', methods=['POST'])
def submit_intake():
    data = request.json
    # Store in session or database
    session['intake_data'] = data
    return jsonify({
        'status': 'success',
        'next_url': f"/pricing/{data.get('industry', 'saas')}"
    })

@app.route('/api/validate-discount', methods=['POST'])
def validate_discount():
    code = request.json.get('code', '').upper()
    
    # Discount codes database
    discounts = {
        'LAUNCH50': {'percent': 50, 'description': 'Launch special - 50% off'},
        'FIRST20': {'percent': 20, 'description': 'First-time client - 20% off'},
        'AFFILIATE15': {'percent': 15, 'description': 'Affiliate partner - 15% off'},
        'HEALTHCARE25': {'percent': 25, 'description': 'Healthcare sector - 25% off'},
    }
    
    if code in discounts:
        return jsonify({
            'valid': True,
            'discount': discounts[code]['percent'],
            'description': discounts[code]['description']
        })
    else:
        return jsonify({'valid': False, 'message': 'Invalid discount code'})

# Health check
@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
