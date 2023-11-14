from PyPDF2 import PdfReader, PdfWriter

# Path to the PDF file and output file
input_pdf_path = './autoactu_annuaire_automobile_15_2024 (2).pdf'
output_pdf_path = './filtered_autoactu_annuaire_automobile_15_2024.pdf'

# Create a PdfReader instance
reader = PdfReader(input_pdf_path)

# Create a PdfWriter instance for the output
writer = PdfWriter()

# Keyword to search for
keyword = "Volume de vente VN"

# Iterate over pages and add pages containing the keyword
for page in reader.pages:
    if keyword in page.extract_text():
        writer.add_page(page)

# Save the filtered PDF
with open(output_pdf_path, "wb") as output_pdf_file:
    writer.write(output_pdf_file)

output_pdf_path

