# PASTE THIS INTO run.py AFTER THE OTHER QUESTIONNAIRE ROUTES

# CUSTOM TIER QUESTIONNAIRE
@app.route('/questionnaire/custom')
def questionnaire_custom():
    return render_template('questionnaire_custom.html')

@app.route('/api/questionnaire/custom', methods=['POST'])
def submit_questionnaire_custom():
    from price_calculator import calculate_monthly_price, get_price_breakdown
    
    form_data = request.form.to_dict()
    features = request.form.getlist('features')  # Multiple checkboxes
    
    # Calculate price
    monthly_price = calculate_monthly_price(
        data_sources=form_data.get('data_sources'),
        frequency=form_data.get('frequency'),
        team_size=form_data.get('team_size'),
        features=features,
        support=form_data.get('support')
    )
    
    # Store in session
    project_id = str(uuid.uuid4())[:8]
    session['project_id'] = project_id
    session['vertical'] = 'custom'
    session['questionnaire_data'] = form_data
    session['features_selected'] = features
    session['custom_monthly_price'] = monthly_price
    session['price_breakdown'] = get_price_breakdown(
        form_data.get('data_sources'),
        form_data.get('frequency'),
        form_data.get('team_size'),
        features,
        form_data.get('support')
    )
    
    # Redirect to checkout with calculated price
    return redirect(f'/checkout/custom/enterprise?price={monthly_price}')
