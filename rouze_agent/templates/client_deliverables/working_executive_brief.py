"""
ROUZE Working Executive Brief Generator
Simplified version that definitely works
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.units import inch
from datetime import datetime

def create_executive_brief():
    # Simple filename
    filename = f"rouze_brief_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
    
    # Create document
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Content
    story.append(Paragraph("ROUZE", styles['Title']))
    story.append(Paragraph("Raw Signals → Real Insights", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    
    story.append(Paragraph("Executive Intelligence Brief", styles['Heading1']))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Key Findings:", styles['Heading2']))
    story.append(Paragraph("• Market opportunity identified through raw signal analysis", styles['Normal']))
    story.append(Paragraph("• Consumer behavior shift detected 3 months ahead of industry recognition", styles['Normal']))
    story.append(Paragraph("• Competitive vulnerability exposed through sentiment analysis", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Strategic Recommendations:", styles['Heading2']))
    story.append(Paragraph("• Launch premium product line within 60 days", styles['Normal']))
    story.append(Paragraph("• Capitalize on competitor weakness in market positioning", styles['Normal']))
    story.append(Paragraph("• Implement authentic sustainability messaging strategy", styles['Normal']))
    story.append(Spacer(1, 0.5*inch))
    
    story.append(Paragraph("Methodology: Raw signal intelligence from social platforms, review analysis, and trend detection", styles['Normal']))
    
    # Build PDF
    doc.build(story)
    return filename

if __name__ == "__main__":
    result = create_executive_brief()
    print(f"Executive brief created: {result}")
