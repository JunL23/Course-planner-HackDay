import os
from flask import Flask, request, jsonify
from google import genai
from PyPDF2 import PdfReader
from io import BytesIO

# Configure the Flask app
app = Flask(__name__)

# --- Configuration ---
# Set your API Key as an environment variable (GEMINI_API_KEY) or set it directly
# For security, using an environment variable is highly recommended.

API_KEY = "AIzaSyCNbYmdptLzQm4974BPUzDbXXIN1KpCkbI"
try:
    # This automatically looks for the GEMINI_API_KEY environment variable
    client = genai.Client(api_key=API_KEY)
except Exception as e:
    print(f"Error initializing Gemini client: {e}")
    # Exit or handle error if key isn't set
    
# Use a fast model for text summarization
MODEL_NAME = 'gemini-2.5-flash' 
# --- End Configuration ---

def extract_text_from_pdf(file_stream):
    """
    Extracts all text from a PDF file stream using PyPDF2.
    """
    try:
        reader = PdfReader(file_stream)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        print(f"PDF extraction error: {e}")
        return None

@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    # 1. Check for the uploaded file
    if 'pdf' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['pdf']
    if file.filename == '' or not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "No selected file or file is not a PDF"}), 400

    # 2. Extract Text
    # Read the file data into a BytesIO buffer for PyPDF2
    file_stream = BytesIO(file.read())
    extracted_text = extract_text_from_pdf(file_stream)

    if not extracted_text:
        return jsonify({"error": "Failed to extract text from PDF. It may be an image-only PDF."}), 500

    # 3. Prepare Prompt for Gemini
    prompt = (
        "You are an expert document reader. Summarize the following document in a clear and concise manner. "
        "Highlight the main purpose and key takeaways. \n\n"
        "--- DOCUMENT TEXT ---\n\n"
        f"{extracted_text}"
    )

    # 4. Call Gemini API
    try:
        print("Sending text to Gemini...")
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        
        # 5. Return the AI's response
        return jsonify({
            "success": True,
            "gemini_response": response.text
        })
        
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return jsonify({"error": f"AI processing failed: {e}"}), 500

if __name__ == '__main__':
    # Add a simple route for the index.html (optional, but good for local testing)
    @app.route('/')
    def index():
        return app.send_static_file('index.html') # Assumes index.html is in a 'static' folder

    # For local development
    # NOTE: You need to ensure index.html is in a 'static' folder 
    # OR change the index route above to load it directly.
    # The frontend code in step 1 assumes the server runs on the same domain/port.
    app.run(debug=True, port=5000)