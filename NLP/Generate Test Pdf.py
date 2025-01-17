from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import yellow, red , blue

def create_test_pdf(output_path):
    c = canvas.Canvas(output_path, pagesize = letter)
    width, height = letter

# Text Content
    c.setFont("Helvetica", 12)
    c.drawString(100, height - 50, "1. Text Content: Plain and Formatted Text")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, height - 70, "This is Bold Text")
    c.setFont("Helvetica-Oblique", 12)
    c.drawString(100, height-90, "This is Italic Text")

#2 Images
    c.drawString(100, height -130,"2. Images: Below is an embedded image.")
    c.drawImage("/home/neuralit/shubham_workarea/shubham_python_workspace/downloads/Iron Man infinity.jpeg",100, height -230, width = 300, height =100)

    #3 HyperLinks
    c.drawString(100, height - 250, "3. Hyperlinks: Click below for OpenAI")
    c.linkURL("https://www.openai.com",(100, height -270, 300, height -250), relative =0)

    #4 Table
    c.drawString(100, height - 300, "4: Table: Simple Table Below")
    data=[["Name","Shubham"],["Age","24"],["Phone","9594070450"]]
    x,y =100, height -320
    for row in data:
        for col in row:
            c.drawString(x,y,col)
            x+=100
        x = 100
        y-= 20

    #5 Annotations (highlighted text)
    c.drawString(100, height -400, "5. Annotations: Hihglighted text example")
    c.setFillColor(yellow)
    c.rect(100, height - 420, 200, 20,fill = True, stroke= False)
    c.setFillColor(blue)
    c.drawString(100, height -415, "This text is highlighted")

    #6 Metadata not available in Report, implelment it using PyPDF2
    
    #7 Iinteractive Forms
    c.drawString(100, height -450, "7. Interactive Forms: See next section for manual additional")

    #8 Embedded Fonts (Defult by Reportlab)
    c.drawString(100, height -470, "8. Fonts: This PDF uses embedded helvetica.")

    #9. Digital Signature

    #10. Shapes and Graphics
    c.drawString(100, height -500, "10. Shapes and Graphics:")
    c.setStrokeColor(red)
    c.rect(100, height -520, 200, 50, fill =0)
    c.line(100, height -520, 300, height -470)

    #11. Content Layout
    c.drawString(100, height - 500, "11. Content Layout: Bounding boxes can be tested separetly.")

    #12. Embedded file sare not supported by Reportlab but can be added using PyPDF2

    #13. Vector Graphics
    c.drawString(100, height - 600, "13. Vector Graphics: Example Circle Below.")
    c.circle(150, height - 650, 30, stroke =1, fill =0)

    #14. Watermarks
    c.saveState()
    c.rotate(45)
    c.setFont("Helvetica-Bold", 36)
    c.setFillColorRGB(0.8, 0.8,0.8)
    c.drawString(200, 0, "Sam Watermark")
    c.restoreState()

    c.showPage()
    c.save()

#Creating the PDF
create_test_pdf("/home/neuralit/shubham_workarea/shubham_python_workspace/export.pdf")