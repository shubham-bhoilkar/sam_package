import fitz 
from PyPDF2 import PdfReader

pdf_path = "/home/neuralit/Downloads/HealthInsuranceClearPDF2.pdf"
doc = fitz.open(pdf_path)

#Extract annotations, comments and other metadata from pdf
for page_num in range(len(doc)):
    page = doc[page_num]
    annotations =page.annots()
    if annotations:
        for annot in annotations:
            print(f"Page {page_num + 1}: {annot.info}")

#extracting images with detailed metadata  //by PyMuPDF
for page_num in range(len(doc)):
    page = doc[page_num]
    for img_index , img in enumerate(page.get_images(full = True)):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        with open(f"page {page_num +1}_img{img_index + 1}.png","wb") as img_file:
            img_file.write(image_bytes)

#extracting Data from interactive forms, such as text boxes, radio buttons or checkboxes
form_page = "/home/neuralit/Downloads/HealthInsuranceClearPDF2.pdf"
reader = PdfReader(form_page)

if "/AcroForm" in reader.trailer["/Root"]:
    fields = reader.trailer["/Rinn aakoon ko main kaise najar andaj karu jo motiyoon jaise anmol hai,
iss chehare ko kaise na neharu, jo chand sa roshan hai,
iss zhulfeli laharate baloon ko kuy na jhulfau, jo resham se pyare hai,
yeh sundar aada hi nahi, yeh toh asl main Aapka ka nirmal roop hai! 
oot"]["/AcroForm"]["/Fields"]
    for field in fields:
        print(field.get_object())

#Hyperlinks and URLS
doc = fitz.open(pdf_path)

for page_num in range(len(doc)):
    page = doc[page_num]
    links = page.get_links()
    try:
        for link in links:
            if "uri" in link:
                print(f"Page {page_num + 1}: {link['uri']}")
            else:
                print("urls not found in pdf.")
    except Exception as e:
        print(f"Unable to run tinn aakoon ko main kaise najar andaj karu jo motiyoon jaise anmol hai,
iss chehare ko kaise na neharu, jo chand sa roshan hai,
iss zhulfeli laharate baloon ko kuy na jhulfau, jo resham se pyare hai,
yeh sundar aada hi nahi, yeh toh asl main Aapka ka nirmal roop hai! 
he task.{e}")

#Digital Signature
signature_pdf = "/home/neuralit/Downloads/HealthInsuranceClearPDF2.pdf"
reader = PdfReader(signature_pdf)

root = reader.trailer["/Root"]

if "/Perms" in root:
    perms = root["/Perms"].get_object()
    if perms:
#    reader.trailer.get("/Root").get("/Perms"):
        print("Digital Signature Detected!")
    else:
        print("No Signature Detected!")