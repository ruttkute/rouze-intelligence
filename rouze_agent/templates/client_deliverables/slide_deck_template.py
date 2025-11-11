"""
ROUZE Slide Deck Generator
Creates professional presentation slides with Rouze branding
"""

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.graphics.shapes import Drawing, Rect
from datetime import datetime

class RouzeSlideDecK:
    def __init__(self, client_name, project_title):
        self.client_name = client_name
        self.project_title = project_title
        self.slides = []
        
        # Rouze brand colors
        self.rouze_cream = HexColor("#F8F6F0")
        self.intelligence_pink = HexColor("#E8C5D1")
        self.signal_black = HexColor("#2C2C2C")
        self.data_gold = HexColor("#D4AF37")
    
    def create_title_slide(self):
        """Professional title slide"""
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'SlideTitle',
            parent=styles['Title'],
            fontSize=36,
            textColor=self.signal_black,
            alignment=1,  # Center
            spaceBefore=2*inch,
            spaceAfter=0.5*inch
        )
        
        subtitle_style = ParagraphStyle(
            'SlideSubtitle',
            parent=styles['Normal'],
            fontSize=16,
            textColor=self.intelligence_pink,
            alignment=1,
            spaceBefore=0,
            spaceAfter=1.5*inch
        )
        
        project_style = ParagraphStyle(
            'ProjectTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=self.signal_black,
            alignment=1,
            spaceBefore=0,
            spaceAfter=0.5*inch
        )
        
        client_style = ParagraphStyle(
            'ClientInfo',
            parent=styles['Normal'],
            fontSize=14,
            textColor=self.signal_black,
            alignment=1
        )
        
        slide_content = [
            Paragraph("𝓡𝓞𝓤𝓩𝓔", title_style),
            Paragraph("Raw Signals → Real Insights", subtitle_style),
            Paragraph(self.project_title, project_style),
            Paragraph(f"Client: {self.client_name}<br/>Date: {datetime.now().strftime('%B %Y')}", client_style)
        ]
        
        return slide_content
    
    def create_overview_slide(self, project_summary):
        """Project overview slide"""
        styles = getSampleStyleSheet()
        
        slide_title_style = ParagraphStyle(
            'OverviewSlideTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=self.signal_black,
            spaceBefore=0.5*inch,
            spaceAfter=0.5*inch
        )
        
        content_style = ParagraphStyle(
            'SlideContent',
            parent=styles['Normal'],
            fontSize=16,
            textColor=self.signal_black,
            spaceBefore=12,
            spaceAfter=12,
            leftIndent=0.5*inch
        )
        
        highlight_style = ParagraphStyle(
            'HighlightBox',
            parent=styles['Normal'],
            fontSize=14,
            textColor=self.signal_black,
            backColor=self.rouze_cream,
            borderPadding=20,
            spaceBefore=20,
            spaceAfter=20
        )
        
        slide_content = [
            Paragraph("Executive Summary", slide_title_style),
            Paragraph(f"<b>Challenge:</b> {project_summary.get('challenge', '')}", content_style),
            Paragraph(f"<b>Methodology:</b> {project_summary.get('methodology', '')}", content_style),
            Paragraph(f"<b>Key Finding:</b> {project_summary.get('key_finding', '')}", highlight_style),
            Paragraph(f"<b>Business Impact:</b> {project_summary.get('business_impact', '')}", content_style)
        ]
        
        return slide_content
    
    def create_insight_slide(self, insight_title, insight_data):
        """Individual insight slide"""
        styles = getSampleStyleSheet()
        
        slide_title_style = ParagraphStyle(
            'InsightSlideTitle',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=self.signal_black,
            spaceBefore=0.5*inch,
            spaceAfter=0.4*inch
        )
        
        signal_style = ParagraphStyle(
            'SignalText',
            parent=styles['Normal'],
            fontSize=14,
            textColor=self.signal_black,
            spaceBefore=8,
            spaceAfter=8,
            leftIndent=0.3*inch
        )
        
        metric_style = ParagraphStyle(
            'MetricHighlight',
            parent=styles['Normal'],
            fontSize=32,
            textColor=self.data_gold,
            alignment=1,
            spaceBefore=0.3*inch,
            spaceAfter=0.3*inch
        )
        
        impact_style = ParagraphStyle(
            'ImpactText',
            parent=styles['Normal'],
            fontSize=15,
            textColor=self.signal_black,
            backColor=self.rouze_cream,
            borderPadding=15,
            spaceBefore=0.2*inch,
            spaceAfter=0.2*inch
        )
        
        slide_content = [
            Paragraph(insight_title, slide_title_style),
            Paragraph(f"<b>Raw Signal Detected:</b>", signal_style),
            Paragraph(insight_data.get('signal', ''), signal_style),
            Paragraph(insight_data.get('metric', ''), metric_style),
            Paragraph(f"<b>Strategic Implication:</b> {insight_data.get('impact', '')}", impact_style),
            Paragraph(f"<b>Recommended Action:</b> {insight_data.get('action', '')}", signal_style)
        ]
        
        return slide_content
    
    def create_methodology_slide(self):
        """Methodology explanation slide"""
        styles = getSampleStyleSheet()
        
        slide_title_style = ParagraphStyle(
            'MethodSlideTitle',
            parent=styles['Heading1'],
            fontSize=22,
            textColor=self.signal_black,
            spaceBefore=0.5*inch,
            spaceAfter=0.4*inch
        )
        
        method_style = ParagraphStyle(
            'MethodText',
            parent=styles['Normal'],
            fontSize=14,
            textColor=self.signal_black,
            spaceBefore=10,
            spaceAfter=10,
            leftIndent=0.3*inch
        )
        
        advantage_style = ParagraphStyle(
            'AdvantageText',
            parent=styles['Normal'],
            fontSize=13,
            textColor=self.signal_black,
            backColor=self.intelligence_pink,
            borderPadding=12,
            spaceBefore=0.2*inch,
            spaceAfter=0.1*inch
        )
        
        slide_content = [
            Paragraph("Rouze Intelligence Methodology", slide_title_style),
            Paragraph("<b>Raw Signal Sources:</b>", method_style),
            Paragraph("• Social media conversations (Reddit, Twitter, TikTok)", method_style),
            Paragraph("• Review platform sentiment analysis", method_style), 
            Paragraph("• Forum discussions and community insights", method_style),
            Paragraph("• News monitoring and trend detection", method_style),
            Spacer(1, 0.2*inch),
            Paragraph("<b>Competitive Advantage:</b> 5-7 day delivery vs 3-6 months traditional research", advantage_style),
            Paragraph("<b>Unique Value:</b> Access to unfiltered consumer signals vs processed survey data", advantage_style)
        ]
        
        return slide_content
    
    def create_closing_slide(self):
        """Professional closing slide"""
        styles = getSampleStyleSheet()
        
        closing_title_style = ParagraphStyle(
            'ClosingTitle',
            parent=styles['Heading1'],
            fontSize=28,
            textColor=self.signal_black,
            alignment=1,
            spaceBefore=1.5*inch,
            spaceAfter=0.5*inch
        )
        
        cta_style = ParagraphStyle(
            'CTAText',
            parent=styles['Normal'],
            fontSize=16,
            textColor=self.signal_black,
            alignment=1,
            spaceBefore=0.3*inch,
            spaceAfter=0.3*inch
        )
        
        footer_style = ParagraphStyle(
            'FooterText',
            parent=styles['Normal'],
            fontSize=12,
            textColor=self.intelligence_pink,
            alignment=1,
            spaceBefore=1*inch
        )
        
        slide_content = [
            Paragraph("Transform Your Market Intelligence", closing_title_style),
            Paragraph("Ready to discover what signals your competitors are missing?", cta_style),
            Spacer(1, 0.5*inch),
            Paragraph("𝓡𝓞𝓤𝓩𝓔 — Raw Signals → Real Insights<br/>Strategic Intelligence Consultancy", footer_style)
        ]
        
        return slide_content
    
    def generate_deck(self, presentation_data, output_filename=None):
        """Generate complete slide deck"""
        if not output_filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            output_filename = f"rouze_deck_{self.client_name}_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(
            output_filename,
            pagesize=landscape(letter),
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        story = []
        
        # Title slide
        story.extend(self.create_title_slide())
        story.append(PageBreak())
        
        # Overview slide
        if 'overview' in presentation_data:
            story.extend(self.create_overview_slide(presentation_data['overview']))
            story.append(PageBreak())
        
        # Insight slides
        for insight in presentation_data.get('insights', []):
            slide_content = self.create_insight_slide(
                insight.get('title', 'Key Insight'),
                insight
            )
            story.extend(slide_content)
            story.append(PageBreak())
        
        # Methodology slide
        story.extend(self.create_methodology_slide())
        story.append(PageBreak())
        
        # Closing slide
        story.extend(self.create_closing_slide())
        
        # Generate PDF
        doc.build(story)
        return output_filename

# Usage example and test
if __name__ == "__main__":
    # Sample presentation data
    sample_presentation = {
        'overview': {
            'challenge': 'Client needed actionable market intelligence beyond generic industry reports',
            'methodology': 'Analyzed 10,000+ raw signals from social platforms and review sites',
            'key_finding': '23% premium pricing opportunity identified through consumer sentiment shift',
            'business_impact': '$380K revenue potential from early market positioning'
        },
        'insights': [
            {
                'title': 'Consumer Sophistication Surge',
                'signal': 'Reddit discussions show 340% increase in "authentic sustainability" mentions over 6 months',
                'metric': '+340%',
                'impact': 'Consumers developing sophisticated detection for fake sustainability claims',
                'action': 'Shift from marketing sustainability to proving measurable impact'
            },
            {
                'title': 'Premium Pricing Window Opens',
                'signal': 'TikTok sentiment analysis reveals Gen-Z willing to pay 23% premium for verified eco-products',
                'metric': '+23%',
                'impact': 'Market positioning opportunity emerging 3-6 months ahead of mainstream recognition',
                'action': 'Launch authentic sustainability line within 60 days for market leadership'
            },
            {
                'title': 'Competitive Vulnerability Detected',
                'signal': 'Major competitor Amazon reviews show 18% increase in "expensive but not green" complaints',
                'metric': '+18%',
                'impact': '3-month strategic window before competitor likely pivots approach',
                'action': 'Capitalize on positioning gap with authentic environmental impact messaging'
            }
        ]
    }
    
    # Generate slide deck
    deck = RouzeSlideDecK("Test Client", "E-commerce Sustainability Intelligence")
    filename = deck.generate_deck(sample_presentation)
    print(f"Slide deck generated: {filename}")