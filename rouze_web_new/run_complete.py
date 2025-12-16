from flask import Flask, render_template, request, redirect, session, jsonify
import os
import uuid
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

# ===== HOME & NAVIGATION =====
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/vertical-selector')
def vertical_selector():
    return render_template('vertical_selector.html')

# ===== QUESTIONNAIRES =====
@app.route('/questionnaire/<vertical>')
def questionnaire(vertical):
    if vertical not in ['healthcare', 'saas', 'ecommerce']:
        return redirect('/vertical-selector')
    return render_template(f'questionnaire_{vertical}.html', vertical=vertical)

@app.route('/api/questionnaire/<vertical>', methods=['POST'])
def submit_questionnaire(vertical):
    if vertical not in ['healthcare', 'saas', 'ecommerce']:
        return redirect('/vertical-selector')
    
    form_data = request.form.to_dict()
    project_id = str(uuid.uuid4())[:8]
    
    session['project_id'] = project_id
    session['vertical'] = vertical
    session['questionnaire_data'] = form_data
    
    return redirect(f'/upload/{vertical}?project_id={project_id}')

# ===== DATA UPLOAD =====
@app.route('/upload/<vertical>')
def upload_form(vertical):
    if vertical not in ['healthcare', 'saas', 'ecommerce']:
        return redirect('/vertical-selector')
    return render_template('upload_form.html', vertical=vertical)

@app.route('/api/upload', methods=['POST'])
def handle_upload():
    vertical = request.form.get('vertical')
    deletion_policy = request.form.get('deletion_policy', 'immediate')
    
    # TODO: Implement actual encryption and file storage
    # For now, just redirect
    
    return jsonify({'success': True})

# ===== FORMAT SELECTION =====
@app.route('/format-selection/<vertical>')
def format_selection(vertical):
    if vertical not in ['healthcare', 'saas', 'ecommerce']:
        return redirect('/vertical-selector')
    return render_template('format_selection.html', vertical=vertical)

# ===== TIER SELECTION =====
@app.route('/tier-selection/<vertical>/<format>')
def tier_selection(vertical, format):
    if vertical not in ['healthcare', 'saas', 'ecommerce']:
        return redirect('/vertical-selector')
    if format not in ['html', 'pdf', 'dashboard', 'api']:
        return redirect(f'/format-selection/{vertical}')
    return render_template('tier_selection.html', vertical=vertical, format=format)

# ===== PAGES =====
@app.route('/methodology')
def methodology():
    return render_template('methodology.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/about')
def about():
    return render_template('about.html')

# ===== ERROR HANDLERS =====
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
