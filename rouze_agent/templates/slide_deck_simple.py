"""
ROUZE Simple Slide Deck Generator
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from datetime import datetime

def create_simple_slide_deck():
    # Simple test that should work
    doc = SimpleDocTemplate(
        "rouze_simple_deck.pdf",
        pagesize=letter,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=inch,
        bottomMargin=inch
    )
    
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'RouzeTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=HexColor("#2C2C2C")
    )
    
    story.append(Paragraph("ROUZE Intelligence", title_style))
    story.append(Paragraph("Raw Signals → Real Insights", styles['Normal']))
    story.append(Spacer(1, 2*inch))
    story.append(Paragraph("Market Intelligence Analysis", styles['Heading1']))
    
    doc.build(story)
    return "rouze_simple_deck.pdf"

if __name__ == "__main__":
    filename = create_simple_slide_deck()
    print(f"Simple deck created: {filename}")