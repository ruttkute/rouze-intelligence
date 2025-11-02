from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)
app.secret_key = 'rouze_secret_key_production'

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/intake/<industry>')
def intake(industry):
    """Intake form"""
    return render_template('intake.html', industry=industry)

@app.route('/health')
def health():
    """Health check"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
