import os
from flask import Flask, request, jsonify, send_file
from google import genai
from google.genai.types import Part
from io import BytesIO
import fitz # PyMuPDF
from PyPDF2 import PdfReader # Kept for optional digital text fallback
from database import init, get_db_connection, get_class


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
    Attempts to extract digital text (for text-based PDFs) as a fast fallback.
    """
    try:
        reader = PdfReader(file_stream)
        text = "".join(page.extract_text() or "" for page in reader.pages)
        file_stream.seek(0) # Reset stream position for the next function (image extraction)
        return text if text.strip() else None
    except Exception as e:
        print(f"Digital text extraction error: {e}. Falling back to image-based OCR.")
        file_stream.seek(0)
        return None
    

def process_image_pdf_with_gemini(file_stream, prompt_text):
    """
    Converts each PDF page to an image and sends it along with the prompt to Gemini.
    """
    try:
        # fitz.open requires the file stream to be read and provided with type
        pdf_bytes = file_stream.read()
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception as e:
        raise ValueError(f"Failed to open PDF document: {e}")

    gemini_parts = []
    
    # 1. Convert Page to Image
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        
        # Increase resolution (3x scale = ~300 DPI) for better OCR accuracy
        pix = page.get_pixmap(matrix=fitz.Matrix(3, 3)) 
        
        # Convert to PNG bytes in memory
        img_bytes = pix.tobytes("png")
        
        # Create a Part object for each image
        gemini_parts.append(
            Part.from_bytes(
                data=img_bytes, 
                mime_type='image/png'
            )
        )
        
        # NOTE: Gemini has a limit on the number of inputs (parts). 
        # For very long PDFs, you might hit this limit or a token limit.
        if len(gemini_parts) > 20: 
             print("Warning: Processing only the first 20 pages to avoid API limits.")
             break 

    # 2. Add the text prompt to the end
    gemini_parts.append(prompt_text)
    
    # 3. Call Gemini API
    print(f"Sending {len(gemini_parts) - 1} page images to Gemini...")
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=gemini_parts
    )
    
    return response.text


@app.route('/process-pdf', methods=['POST'])
def process_pdf():
    init()
    if 'pdf' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['pdf']
    if file.filename == '' or not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "No selected file or file is not a PDF"}), 400

    # Read the file data into a BytesIO buffer
    file_stream = BytesIO(file.read())
    
    # Prompt for Gemini
    prompt = (
        "For the following document I want you to extract primarily from the page consisting of major requirements and extra major requirements."
        "take note of the specific class codes, and numbers do not list the amount of credits each class is worth only the total credits required for the major."
        "give your response in plain text using only letters, numbers, spaces, and parenthesis"


        "when displaying a class do not seperate the code and number with a space example: BIO100 not BIO 100"
        "for response give an overview which includes the amount of credits required for the major"
        "give another section of core classes that cannot be skipped this should be labeled 'core classes', and a list of additional major requirements if present"
        "If a requirement lists the poissibility of 2 classes put them on the same line as 'class1 OR class2'  if more than 2 classes are present use commas to seperate them and the class code make sure that the last class ALSO HAS A COMMA, keep all classes on one line"
        "if a class has a '/' in between 2 numbers list them as both classes with 'AND' in between. example: 100/200 should be listed as 100 AND 200"
        "if a class has a '/' in between 2 class codes only name one that has a matching code to the core class codes. example: PHY/SCI 100 should be listed as PHY 100"
        "for any section that specifies an amount of classes from a list, after listing the classes in parenthesis add 'choose X from the following' where X is the amount of classes required"
        "for any line that does not have a class code in it list it as 'major notes'"


    )

    try:
        # Use the multimodal function which handles OCR internally
        gemini_response = process_image_pdf_with_gemini(file_stream, prompt)
        lines = gemini_response.split('\n')
        
        sub_list = []
        amount_to_choose = 1
        for line_ind in range(len(lines)):
            if ',' in lines[line_ind]:
                sub_list = lines[line_ind].split(',')
                print(sub_list[-1][:5])
                if sub_list[-1][:5] == ' (cho':
                    amount_to_choose = int(sub_list[-1][9])
                lines[line_ind] = sub_list = lines[line_ind].split(',')[:amount_to_choose]
                print(amount_to_choose)
                amount_to_choose = 1
            if 'OR' in lines[line_ind]:
                lines[line_ind] = lines[line_ind].split('OR')[0].strip()



        for line in lines:
            if isinstance(line, list):
                for item in line:
                    course = get_class(item.strip())
                    if course is not None:
                        joined = '. '.join(str(x) for x in course)
                        print(item)
                    else:
                        print(f"Course not found for: {item}")
            else:
                course = get_class(line.strip())
                if course is not None:
                    joined = '. '.join(str(x) for x in course)
                    print(line)
                else:
                    print(f"Course not found for: {line}")
        
        prompt_2 = (
            "given the following classes we know we need, generate a schedule that doesn't bypass pre requisites."
            "following classes are needed: " + joined + "where the information is formatted is the 'class code, class credits, class pre requisites, gen_ed'"
            "the schedule should have no more than 19 credits per semester and generate 8 semesters"
        )

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt_2
        )

        # Return the AI's response
        return jsonify({
            "success": True,
            "gemini_response": response
        })
        
    except Exception as e:
        print(f"Processing Failed: {e}")
        return jsonify({"error": f"File processing or AI failed: {e}"}), 500
        
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