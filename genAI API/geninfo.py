from flask import Flask, jsonify, request
from PIL import Image
import google.generativeai as genai
import os

app = Flask(__name__)

# Configure the Google Generative AI
genai.configure(api_key="AIzaSyBWRwQPKmCA2_uXLorJj8aSGRSk3VhjmbQ")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# The function that processes the image and calls the generative model
def GetAns():
    # Open the image (hardcoded path)
    img_path = r"C:\Users\leris\OneDrive\Documents\Desktop\datasetCreation\temp_image.jpg"
    img = Image.open(img_path)
    
    # Generate the response using the Google model
    response = model.generate_content([
        "Give the invoice number, invoice date, invoice amount, buyer gstin, supplier gstin in one python list from the given image in the same order. The output should only be a python list of the values I asked for.",
        img
    ])
    return response.text

# Flask route to expose the function
@app.route('/get-invoice-details', methods=['POST'])
def get_invoice_details():
    try:
        # Call the GetAns function to process the image
        result = GetAns()
        
        # Return the result as a JSON response
        return jsonify({'response': result}), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask app locally
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
