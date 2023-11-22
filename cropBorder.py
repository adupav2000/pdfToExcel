from PyPDF2 import PdfReader, PdfWriter
import os
import glob

def crop_pdf_borders(pdf_path, output_path, margins):
    """
    Crops the borders of a PDF file.

    :param pdf_path: The path to the input PDF file.
    :param output_path: The path to the output cropped PDF file.
    :param margins: A dictionary with 'top', 'bottom', 'left', 'right' margins to crop.
    """
    # Load the PDF file
    pdf_reader = PdfReader(pdf_path)
    pdf_writer = PdfWriter()

    # Go through each page in the PDF
    for page in pdf_reader.pages:
        # Get the page dimensions
        page_width = page.mediabox.width
        page_height = page.mediabox.height

        # Calculate new borders
        lower_left_x = margins['left']
        lower_left_y = margins['bottom']
        upper_right_x = page_width - margins['right']
        upper_right_y = page_height - margins['top']

        # Set the new page boundaries (crop the page)
        page.cropbox.lower_left = (lower_left_x, lower_left_y)
        page.cropbox.upper_right = (upper_right_x, upper_right_y)

        # Add the cropped page to the writer object
        pdf_writer.add_page(page)

    # Write the cropped PDF to the output file
    with open(output_path, 'wb') as f_out:
        pdf_writer.write(f_out)

# New function to crop all PDFs in a folder
def crop_all_pdfs_in_folder(folder_path, margins):
    # Find all PDF files in the specified directory
    pdf_files = glob.glob(os.path.join(folder_path, '*.pdf'))

    # Loop through all found PDF files and crop them
    for pdf_file in pdf_files:
        print("Processing : ", pdf_file)
        file_name, file_extension = os.path.splitext(pdf_file)
        output_file = f"{file_name}_cropped{file_extension}"
        crop_pdf_borders(pdf_file, output_file, margins)

# Specify the directory containing the PDF files
folder_path = 'splitAndFilteredPDF'  # Replace with the actual path to your PDF directory

# Define the margins to crop (in points; 1 point = 1/72 inch)
margins_to_crop = {'top': 20, 'bottom': 40, 'left': 40, 'right': 40}

# Crop all PDFs in the folder
crop_all_pdfs_in_folder(folder_path, margins_to_crop)