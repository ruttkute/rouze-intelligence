import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from weasyprint import HTML, CSS
from jinja2 import Template
import json
from datetime import datetime

class RouzePDFGenerator:
    def __init__(self):
        # Rouze brand colors
        self.colors = {
            'cream': '#F8F6F0',
            'pink': '#E8C5D1', 
            'black': '#2C2C2C',
            'gold': '#D4AF37',
            'gray': '#8B8B8B'
        }
        
    def generate_executive_brief(self, data, output_path):
        """Generate executive brief PDF using WeasyPrint"""
        template = self._get_executive_template()
        html_content = template.render(
            client_name=data.get('client_name', 'Client'),
            project_title=data.get('project_title',