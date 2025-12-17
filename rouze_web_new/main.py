from flask import Flask, render_template, request, redirect, jsonify
from datetime import datetime
import uuid
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rouze_secret_key_2025'

# HOME & MAIN PAGES
@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/vertical-selector', methods=['GET'])
def vertical_selector():
    return render_template('vertical_selector.html')

@app.route('/methodology', methods=['GET'])
def methodology():
    return render_template('methodology.html')

@app.route('/security', methods=['GET'])
def security():
    return render_template('security.html')

@app.route('/case-studies', methods=['GET'])
def case_studies():
    return render_template('case_studies.html')

@app.route('/pricing', methods=['GET'])
def pricing():
    return render_template('pricing.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/faq', methods=['GET'])
def faq():
    return render_template('faq.html')

@app.route('/terms', methods=['GET'])
def terms():
    return render_template('terms.html')

@app.route('/privacy', methods=['GET'])
def privacy():
    return render_template('privacy.html')

@app.route('/account', methods=['GET'])
def account():
    return render_template('account.html')

# QUESTIONNAIRE ROUTES
@app.route('/questionnaire/healthcare', methods=['GET'])
def questionnaire_healthcare():
    return render_template('questionnaire_healthcare.html')

@app.route('/questionnaire/healthcare', methods=['POST'])
def api_questionnaire_healthcare_submit():
    project_id = str(uuid.uuid4())[:8]
    return redirect(f'/upload?vertical=healthcare&project_id={project_id}')

@app.route('/questionnaire/saas', methods=['GET'])
def questionnaire_saas():
    return render_template('questionnaire_saas.html')

@app.route('/questionnaire/saas', methods=['POST'])
def api_questionnaire_saas_submit():
    project_id = str(uuid.uuid4())[:8]
    return redirect(f'/upload?vertical=saas&project_id={project_id}')

@app.route('/questionnaire/ecommerce', methods=['GET'])
def questionnaire_ecommerce():
    return render_template('questionnaire_ecommerce.html')

@app.route('/questionnaire/ecommerce', methods=['POST'])
def api_questionnaire_ecommerce_submit():
    project_id = str(uuid.uuid4())[:8]
    return redirect(f'/upload?vertical=ecommerce&project_id={project_id}')

@app.route('/questionnaire/fintech', methods=['GET'])
def questionnaire_fintech():
    return render_template('questionnaire_fintech.html')

@app.route('/questionnaire/fintech', methods=['POST'])
def api_questionnaire_fintech_submit():
    project_id = str(uuid.uuid4())[:8]
    return redirect(f'/upload?vertical=fintech&project_id={project_id}')

@app.route('/questionnaire/realestate', methods=['GET'])
def questionnaire_realestate():
    return render_template('questionnaire_realestate.html')

@app.route('/questionnaire/realestate', methods=['POST'])
def api_questionnaire_realestate_submit():
    project_id = str(uuid.uuid4())[:8]
    return redirect(f'/upload?vertical=realestate&project_id={project_id}')

# DATA UPLOAD & FORMAT SELECTION
@app.route('/upload', methods=['GET'])
def upload():
    return render_template('data_upload.html')

@app.route('/upload', methods=['POST'])
def api_upload_submit():
    vertical = request.args.get('vertical', request.form.get('vertical', 'healthcare'))
    project_id = request.args.get('project_id', str(uuid.uuid4())[:8])
    return redirect(f'/format-selection?vertical={vertical}&project_id={project_id}')

@app.route('/format-selection', methods=['GET'])
def format_selection():
    return render_template('format_selection.html')

@app.route('/format-selection', methods=['POST'])
def api_format_selection_submit():
    vertical = request.args.get('vertical', 'healthcare')
    project_id = request.args.get('project_id', str(uuid.uuid4())[:8])
    return redirect(f'/checkout?vertical={vertical}&project_id={project_id}')

# CHECKOUT
@app.route('/checkout', methods=['GET'])
def checkout():
    return render_template('checkout.html')

@app.route('/checkout', methods=['POST'])
def api_checkout_submit():
    project_id = request.args.get('project_id', str(uuid.uuid4())[:8])
    return redirect(f'/analysis?project_id={project_id}')

# ANALYSIS PROCESSING
@app.route('/analysis', methods=['GET'])
def analysis_processing():
    return render_template('analysis.html')

# DASHBOARD
@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.html')

# ERROR HANDLERS
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
