from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from PyPDF2 import PdfReader, PdfWriter

# Define the output PDF path
output_pdf = "comprehensive_pdf_demo.pdf"

# Create a PDF with ReportLab
def create_pdf():
    c = canvas.Canvas(output_pdf, pagesize=letter)
    width, height = letter

    # 1. Add Text Content
    c.drawString(100, height - 50, "1. Text Content: This is an example of plain text.")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, height - 70, "Formatted Text: Bold Text Example.")

    # 2. Add an Image
    c.drawImage("/home/neuralit/shubham_workarea/shubham_python_workspace/downloads/Iron Man.png", 100, height - 150, width=200, height=100)

    # 3. Add a Hyperlink (annotated as text for illustration)
    c.drawString(100, height - 180, "3. Hyperlink: Visit OpenAI at https://www.openai.com")

    # 4. Add a Table
    data = [["Header 1", "Header 2", "Header 3"], ["Data 1", "Data 2", "Data 3"]]
    table = Table(data, colWidths=[100] * 3, rowHeights=[20] * 2)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    table.wrapOn(c, width, height)
    table.drawOn(c, 100, height - 250)

    # 5. Add Metadata
    c.drawString(100, height - 280, "5. Metadata: Author - Your Name")

    # 6. Add Form Elements Placeholder (as text description, forms require different tools)
    c.drawString(100, height - 300, "6. Form Elements Placeholder: Text fields, checkboxes, etc.")

    # 7. Add Vector Graphics
    c.setStrokeColor(colors.blue)
    c.setLineWidth(3)
    c.line(100, height - 350, 300, height - 350)  # Line
    c.circle(200, height - 400, 50)  # Circle

    # 8. Add Watermark Placeholder (Text as example)
    c.drawString(100, height - 450, "8. Watermark: Confidential")

    # Finalize the PDF
    c.save()

# Add Digital Signature Placeholder
def add_signature_placeholder():
    reader = PdfReader(output_pdf)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Add a blank page with signature text placeholder
    from PyPDF2.generic import AnnotationBuilder

    writer.add_metadata(reader.metadata)

    # Save final output
    with open(output_pdf, "wb") as f:
        writer.write(f)

if __name__ == "__main__":
    create_pdf()
