"""
Vertical Selector Route
Routes user to correct questionnaire based on industry selection
"""
from flask import render_template, redirect
from app import app

@app.route('/vertical-selector')
def vertical_selector():
    """Display vertical selector page"""
    return render_template('vertical_selector.html')

@app.route('/select-vertical/<vertical>')
def select_vertical(vertical):
    """Redirect to questionnaire based on selected vertical"""
    valid_verticals = ['healthcare', 'saas', 'ecommerce']
    
    if vertical.lower() not in valid_verticals:
        return redirect('/vertical-selector')
    
    return redirect(f'/questionnaire/{vertical.lower()}')
