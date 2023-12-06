import os
import fitz  # PyMuPDF
import requests
import json
from openai import OpenAI
client = OpenAI()

# Your OpenAI API key

# Directory containing PDF files
pdf_folder = "C:\\Nouveau dossier\\cleanedPDFForV2"

# Environment variable for OpenAI API key
api_key = os.environ.get('OPENAI_API_KEY')
api_key = "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"
response_folder = "AllResponsesInJsonv2"

# Ensure the response folder exists
os.makedirs(response_folder, exist_ok=True)

# Function to save response in JSON format
def save_response_as_json(response, filename):
    try:
        # Attempt to convert the response to JSON
        response_json = response
        file_path = os.path.join(response_folder, f"{filename}.json")

        # Save the JSON file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(response_json, f, ensure_ascii=False, indent=4)
        print(f"Saved with no issues the file filename.")
    except ValueError as e:
        # Print error if the response is not JSON-formattable
        print(f"Error: The response content for '{filename}' is not JSON-formattable. Error details: {e}")

# api_key = "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"
# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)

    text = """
        Given the french text you have here, please extract the following information, only using a json format:
   {
    "Nom du groupe": "..."
    "Nom de la holding": "...",
    "Mails": ["...", "..."],
    "Téléphone du groupe": ["..."],
    "Chiffre d'affaire 2022": "...",
    "Résumé en bref": "",
    "Nom du DAF" : "..."
    },
  Once you are done with filling this information and gave back this format. Please stop writting. 
  Do not write anything else that this in the response. If there is any other information add it in the list.
  If you find other informations add them to the json. It is possible that some of the information is not available, please leave the field empty when it is the case.
  Only write information you have medium to high confidence in.

    """
    for page in doc:
        text += page.get_text()
    doc.close()
    return text

# Function to send text to ChatGPT API and format response
def query_chatgpt(text):
    response = client.chat.completions.create(
    model="gpt-4",
    temperature=0.1,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": text + " \n\n"}
    ]
    )
    return response

i = 0
# Main process
for filename in os.listdir(pdf_folder):
    if filename.lower().endswith('.pdf'):
        i = i + 1
        if (i < 100):
            continue
        pdf_path = os.path.join(pdf_folder, filename)
        pdf_text = extract_text_from_pdf(pdf_path)
        
        # Define the specific JSON format you want here
        formatted_text = {
            "filename": filename,
            "content": pdf_text
        }

        # Sending text to ChatGPT API
        response = query_chatgpt(json.dumps(formatted_text))
        
        print(response)
        content_to_save = response.choices[0].message.content
        # Save the response content in the predefined folder
        save_response_as_json(content_to_save, filename)