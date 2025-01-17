import fitz
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

#Extracting Rough Data from PDF
def extract_data_from_pdf(pdf_path):
    extracted_data_from_pdf ={
        "text_content": [],
        "images":[],
        "links":[]
    }
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc[page_num]
        
        text = page.get_text()
        extracted_data_from_pdf["text_content"].append({"page":page_num + 1,"text":text})

        for img_index, img in enumerate(page.get_images(full = True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            extracted_data_from_pdf["images"].append({
                "page":page_num +1,
                "index": img_index,
                "image_bytes":image_bytes
            })
        
        #Extracting Images
        for img_index, img in enumerate(page.get_images(full= True)):
            xref = img [0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            extracted_data_from_pdf["images"].append({
                "page":page_num + 1,
                "index": img_index,
                "image_bytes":image_bytes
            })

        #Extracting Links
        for link in page.get_links():
            if "uri" in link:
                extracted_data_from_pdf["links"].append({"page":page_num + 1, "uri":link["uri"]})
        
    doc.close()
    return extracted_data_from_pdf

def create_structured_pdf(output_path, extracted_data):
    c= canvas.Canvas(output_path, pagesize =letter)
    width, height = letter

    #ADDING Text content  
    y_position = height -50
    c.setFont("Helvetica", 12)
    c.drawString(100, y_position, "1. Extracted Text Content:")
    for item in extracted_data["text_content"]:
        y_position -= 20
        text = f"Page {item['page']}: {item['text'][:100]}........."    #Truncate for brevity
        c.drawString(100, y_position, text)
        if y_position < 100:
            c.showPage()
            y_position = height -50

    #Adding Images
    c.showPage()
    y_position = height - 50
    c.drawString(100, y_position, "2. Extracted Images: ")
    for img_data in extracted_data["images"]:
        y_position -= 120
        if y_position < 100:
            c.showPage()
            y_position -= height - 50
        img_path = f"temp_image_page{img_data['page']}_index{img_data['index']}.png"
        with open(img_path, "wb") as img_file:
            img_file.write(img_data["image_bytes"])
        c.drawImage(img_path, 100, y_position, width =100, height =100)

    #Adding Hyperlinks
    c.showPage()
    y_position = height - 50
    c.drawString(100, y_position, "3. Extracted Hypelimks:")
    for link_data in extracted_data["links"]:
        y_position -= 20
        link_text = f"Page {link_data['page']}:{link_data['uri']}"
        c.drawString(100, y_position, link_text)
        if y_position < 100:
            c.showPage()
            y_position= height - 50

    c.save()

rough_pdf_path = "/home/neuralit/shubham_workarea/shubham_python_workspace/export   .pdf"
output_pdf_path = "Customed output.pdf"

extracted_data =extract_data_from_pdf(rough_pdf_path)
create_structured_pdf(output_pdf_path, extracted_data)

print(f"Structured Customed PDF Created Successfully: {output_pdf_path}")