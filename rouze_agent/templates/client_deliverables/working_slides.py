"""
ROUZE Working Slide Generator
Creates basic presentation slides
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from datetime import datetime

def create_slide_deck():
    filename = f"rouze_slides_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    
    # Use standard letter size (no landscape to avoid import issues)
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Slide 1: Title
    story.append(Paragraph("ROUZE", styles['Title']))
    story.append(Paragraph("Raw Signals → Real Insights", styles['Normal']))
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("Market Intelligence Analysis", styles['Heading1']))
    story.append(PageBreak())
    
    # Slide 2: Key Insight
    story.append(Paragraph("Key Insight #1", styles['Heading1']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Consumer Behavior Shift Detected", styles['Heading2']))
    story.append(Paragraph("Raw Signal: 340% increase in authentic sustainability discussions", styles['Normal']))
    story.append(Paragraph("Business Impact: Premium pricing opportunity identified", styles['Normal']))
    story.append(PageBreak())
    
    # Slide 3: Recommendations
    story.append(Paragraph("Strategic Recommendations", styles['Heading1']))
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("1. Launch authentic sustainability line within 60 days", styles['Normal']))
    story.append(Paragraph("2. Implement premium pricing strategy", styles['Normal']))
    story.append(Paragraph("3. Capitalize on 3-month market advantage window", styles['Normal']))
    
    doc.build(story)
    return filename

if __name__ == "__main__":
    result = create_slide_deck()
    print(f"Slide deck created: {result}")
