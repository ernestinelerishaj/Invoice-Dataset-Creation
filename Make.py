import streamlit as st 
from doctr.io import DocumentFile
from doctr.models import ocr_predictor
import re
import json 
import requests
import ast
import os 

# Define the URL for your Flask API
url = "http://localhost:5000/get-invoice-details"

def get_invoice_details():
    try:
        response = requests.post(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Get the JSON response from the API
            data = response.json()
            
            response_list = ast.literal_eval(data['response'])
            return response_list
            
        else:
            print(f"Failed to get response from API. Status code: {response.status_code}")
            print("Error message:", response.json().get('error', 'No error message provided'))
            
    except Exception as e:
        return 


def clean_text(text):
    # Clean and format the text as required
    # Remove unnecessary whitespace, symbols, and preprocess it for easier extraction
    cleaned_text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Removing non-ASCII characters
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)  # Remove excess whitespace
    return cleaned_text
def write(data):
    # File path for the JSON file
    file_path = "dataset.json"
    
    # Check if the file exists
    if os.path.exists(file_path):
        # Open the file and load existing data
        with open(file_path, "r") as f:
            try:
                # Load existing data
                file_data = json.load(f)
            except json.JSONDecodeError:
                # If the file is empty or contains invalid JSON, start with an empty list
                file_data = []
    else:
        # If the file doesn't exist, create an empty list to store data
        file_data = []
    
    # Add the new data to the existing data
    file_data.append(data)
    
    # Write the updated data back to the file
    with open(file_path, "w") as f:
        json.dump(file_data, f, indent=4)

data={
        "invoice_number": None,
        "invoice_date": None,
        "invoice_amount": None,
        "buyer_gstin": None,
        "supplier_gstin": None,
        "text":None
}

file=st.file_uploader("Image")

if file:
    temp_file_path = "temp_image.jpg"  # You can give it any name with the correct extension
    
    # Write the uploaded image to a temporary file
    with open(temp_file_path, "wb") as f:
        f.write(file.getbuffer())
    st.image(file)
    values=get_invoice_details()
    data["invoice_number"]=st.text_input("Invoice number",value=values[0])
    data["invoice_date"]=st.text_input("Invoice date",value=values[1])
    data["invoice_amount"]=st.text_input("Invoice amount",value=values[2])
    data["buyer_gstin"]=st.text_input("Buyer GSTIN",value=values[3])
    data['supplier_gstin']=st.text_input("Supplier GSTIN",value=values[4])
    
    if st.button("Done"):
        #Perform doctr
        doc = DocumentFile.from_images("temp_image.jpg")
        # Initialize OCR model
        model = ocr_predictor(pretrained=True)

        # Perform OCR
        result = model(doc)

        # Get the extracted text
        extracted_text = result.render() 
        cleanData=clean_text(extracted_text)
        data["text"]=cleanData
        write(data)