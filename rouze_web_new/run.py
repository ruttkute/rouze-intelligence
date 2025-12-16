from flask import Flask, render_template, jsonify
from flask import Flask, render_template, request, redirect, session, jsonify
import os
import uuid
from price_calculator import calculate_monthly_price, get_price_breakdown

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-key-change-in-production')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/vertical-selector')
def vertical_selector():
    return render_template('vertical_selector.html')

@app.route('/questionnaire/<vertical>')
def questionnaire(vertical):
    if vertical not in ['healthcare', 'saas', 'ecommerce', 'custom']:
        return redirect('/vertical-selector')
    return render_template(f'questionnaire_{vertical}.html', vertical=vertical)

@app.route('/api/questionnaire/<vertical>', methods=['POST'])
def submit_questionnaire(vertical):
    if vertical not in ['healthcare', 'saas', 'ecommerce', 'custom']:
        return redirect('/vertical-selector')
    
    form_data = request.form.to_dict()
    project_id = str(uuid.uuid4())[:8]
    session['project_id'] = project_id
    session['vertical'] = vertical
    session['questionnaire_data'] = form_data
    
    # CUSTOM TIER: Calculate price
    if vertical == 'custom':
        features = request.form.getlist('features')
        
        # Get form values
        data_sources = form_data.get('data_sources', 'standard')
        frequency = form_data.get('frequency', 'one_time')
        team_size = form_data.get('team_size', 'small')
        support = form_data.get('support', 'email')
        
        # Calculate price
        monthly_price = calculate_monthly_price(
            data_sources=data_sources,
            frequency=frequency,
            team_size=team_size,
            features=features,
            support=support
        )
        
        # Get breakdown
        price_breakdown = get_price_breakdown(
            data_sources=data_sources,
            frequency=frequency,
            team_size=team_size,
            features=features,
            support=support
        )
        
        # Store in session
        session['custom_monthly_price'] = monthly_price
        session['price_breakdown'] = price_breakdown
        session['features_selected'] = features
        session['data_sources'] = data_sources
        session['frequency'] = frequency
        session['team_size'] = team_size
        session['support'] = support
        
        return redirect(f'/checkout/custom/enterprise')
    
    # Standard tiers: go to upload
    return redirect(f'/upload/{vertical}?project_id={project_id}')

@app.route('/upload/<vertical>')
def upload_form(vertical):
    if vertical not in ['healthcare', 'saas', 'ecommerce']:
        return redirect('/vertical-selector')
    return render_template('upload_form.html', vertical=vertical)

@app.route('/api/upload', methods=['POST'])
def handle_upload():
    vertical = request.form.get('vertical')
    deletion_policy = request.form.get('deletion_policy', 'immediate')
    session['deletion_policy'] = deletion_policy
    return redirect(f'/format-selection/{vertical}')

@app.route('/format-selection/<vertical>')
def format_selection(vertical):
    if vertical not in ['healthcare', 'saas', 'ecommerce']:
        return redirect('/vertical-selector')
    return render_template('format_selection.html', vertical=vertical)

@app.route('/api/format-selection/<vertical>', methods=['POST'])
def save_format_selection(vertical):
    if vertical not in ['healthcare', 'saas', 'ecommerce']:
        return redirect('/vertical-selector')
    format_choice = request.form.get('format', 'html_interactive')
    session['format'] = format_choice
    session['dashboard_upgrade'] = request.form.get('dashboard_upgrade', 'no')
    session['api_upgrade'] = request.form.get('api_upgrade', 'no')
    return redirect(f'/tier-selection/{vertical}')

@app.route('/tier-selection/<vertical>')
def tier_selection(vertical):
    if vertical not in ['healthcare', 'saas', 'ecommerce']:
        return redirect('/vertical-selector')
    format_choice = session.get('format', 'html_interactive')
    return render_template('tier_selection.html', vertical=vertical, format=format_choice)

@app.route('/checkout/<vertical>/<tier>')
def checkout(vertical, tier):
    if vertical not in ['healthcare', 'saas', 'ecommerce', 'custom']:
        return redirect('/vertical-selector')
    if tier not in ['quick', 'strategic', 'predictive', 'enterprise']:
        return redirect(f'/tier-selection/{vertical}')
    
    # CUSTOM TIER: Pass calculated price to template
    if vertical == 'custom' and tier == 'enterprise':
        custom_monthly_price = session.get('custom_monthly_price', 5000)
        price_breakdown = session.get('price_breakdown', {})
        features = session.get('features_selected', [])
        
        return render_template('checkout.html',
                             vertical=vertical,
                             tier=tier,
                             is_custom=True,
                             custom_monthly_price=custom_monthly_price,
                             price_breakdown=price_breakdown,
                             features_selected=features)
    
    # Standard tiers
    format_choice = session.get('format', 'html_interactive')
    dashboard_upgrade = session.get('dashboard_upgrade', 'no')
    api_upgrade = session.get('api_upgrade', 'no')
    
    return render_template('checkout.html',
                         vertical=vertical,
                         tier=tier,
                         format=format_choice,
                         dashboard_upgrade=dashboard_upgrade,
                         api_upgrade=api_upgrade)

@app.route('/dashboard/<project_id>')
def dashboard(project_id):
    return render_template('dashboard.html', project_id=project_id)

@app.route('/methodology')
def methodology():
    return render_template('methodology.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5001)

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')
