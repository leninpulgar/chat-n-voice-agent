from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import os

def create_sample_pdf():
    """Create a sample PDF from the business info text file."""
    
    # Read the sample business info
    with open("sample_business_info.txt", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Create PDF
    doc = SimpleDocTemplate("business_info.pdf", pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Split content into lines and create paragraphs
    lines = content.split('\n')
    
    for line in lines:
        if line.strip():
            if line.startswith('='):
                # Header line
                continue
            elif line.isupper() and ':' in line:
                # Section headers
                story.append(Paragraph(line, styles['Heading2']))
            elif line.startswith('Business Name:'):
                # Business name as title
                story.append(Paragraph(line.replace('Business Name: ', ''), styles['Title']))
            else:
                # Regular text
                story.append(Paragraph(line, styles['Normal']))
        else:
            story.append(Spacer(1, 12))
    
    # Build PDF
    doc.build(story)
    print("Sample PDF created: business_info.pdf")

def simple_pdf_creator():
    """Create a simple PDF without reportlab (fallback method)."""
    try:
        # Try to use reportlab first
        create_sample_pdf()
    except ImportError:
        print("reportlab not available, creating simple text-based PDF...")
        # For this demo, we'll just copy the text file
        # In a real scenario, you'd want to use a PDF library
        import shutil
        shutil.copy("sample_business_info.txt", "business_info.txt")
        print("Created business_info.txt (use this as text file for testing)")

if __name__ == "__main__":
    simple_pdf_creator()
