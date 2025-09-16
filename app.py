from flask import Flask, render_template, request, flash, redirect, url_for 
from werkzeug.utils import secure_filename 
import os 
import re 
from PyPDF2 import PdfReader 
from PIL import Image 
import pytesseract 
 
app = Flask(__name__) 
app.secret_key = 'your_secret_key_here' 
 
UPLOAD_FOLDER = 'static/uploads' 
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'} 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
 
if not os.path.exists(UPLOAD_FOLDER): 
    os.makedirs(UPLOAD_FOLDER) 
 
def allowed_file(filename): 
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 
 
def extract_text_from_pdf(pdf_file): 
    """Extract text from a PDF file""" 
    try: 
        reader = PdfReader(pdf_file) 
        text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()]) 
        return text 
    except Exception as e: 
        raise Exception(f"Error reading PDF: {str(e)}") 
 
def extract_text_from_image(image_file): 
    """Extract text from an image using OCR""" 
 
    try: 
        image = Image.open(image_file) 
        text = pytesseract.image_to_string(image) 
        return text 
    except Exception as e: 
        raise Exception(f"Error processing image: {str(e)}") 
 
def extract_drug_names(text): 
    """Extract potential drug names from text using regex.""" 
    words = re.findall(r'\b[A-Z][a-z]+(?: [A-Z][a-z]+)?\b', text)  # Capitalized words assumed as drug names 
    return set(words) 
 
def get_sentence_differences(text1, text2): 
    """Extract sentence differences between two texts""" 
    sentences1 = re.split(r'[.!?]+', text1) 
    sentences2 = re.split(r'[.!?]+', text2) 
     
    # Clean and filter empty sentences 
    sentences1 = [s.strip() for s in sentences1 if s.strip()] 
    sentences2 = [s.strip() for s in sentences2 if s.strip()] 
     
    missing_sentences = [s for s in sentences1 if s not in sentences2] 
    extra_sentences = [s for s in sentences2 if s not in sentences1] 
     
    return missing_sentences, extra_sentences 
 
@app.route('/') 
@app.route('/home') 
def home(): 
    return render_template('home.html') 
 
@app.route('/analyze', methods=['POST']) 
def analyze(): 
    try: 
        # Process original input 
 
        original_input_type = request.form.get('input_type') 
        original_text = request.form.get('original_report', '') 
        original_file = None 
 
        if original_input_type in ['pdf', 'image']: 
            file_key = f'original_{original_input_type}' 
            if file_key in request.files: 
                original_file = request.files[file_key] 
                if not original_file or not allowed_file(original_file.filename): 
                    flash(f'Invalid or missing {original_input_type} file for original report', 'danger') 
                    return redirect(url_for('home')) 
 
        # Process transcribed input 
        wrong_input_type = request.form.get('wrong_input_type') 
        wrong_text = request.form.get('wrong_report', '') 
        wrong_file = None 
 
        if wrong_input_type in ['pdf', 'image']: 
            file_key = f'wrong_{wrong_input_type}' 
            if file_key in request.files: 
                wrong_file = request.files[file_key] 
                if not wrong_file or not allowed_file(wrong_file.filename): 
                    flash(f'Invalid or missing {wrong_input_type} file for transcription', 'danger') 
                    return redirect(url_for('home')) 
 
        # Extract text from both inputs 
        original_text = extract_text_from_pdf(original_file) if original_input_type == 'pdf' else 
extract_text_from_image(original_file) if original_input_type == 'image' else original_text 
        wrong_text = extract_text_from_pdf(wrong_file) if wrong_input_type == 'pdf' else 
extract_text_from_image(wrong_file) if wrong_input_type == 'image' else wrong_text 
 
        if not original_text or not wrong_text: 
            flash('Please provide both original and transcribed content', 'danger') 
            return redirect(url_for('home')) 
 
 
        # Extract and compare drug names 
        original_drugs = extract_drug_names(original_text) 
        transcribed_drugs = extract_drug_names(wrong_text) 
 
        missing_drugs = original_drugs - transcribed_drugs 
        extra_drugs = transcribed_drugs - original_drugs 
 
        # Get wrong and extra sentences 
        missing_sentences, extra_sentences = get_sentence_differences(original_text, wrong_text) 
 
        # Calculate similarity percentage based on drug names 
        all_drugs = original_drugs | transcribed_drugs 
        matching_drugs = original_drugs & transcribed_drugs 
 
        similarity_percentage = (len(matching_drugs) / len(all_drugs) * 100) if all_drugs else 0 
 
        return render_template('away.html', 
                               original_text=original_text, 
                               wrong_text=wrong_text, 
                               missing_drugs=missing_drugs, 
                               extra_drugs=extra_drugs, 
                               missing_sentences=missing_sentences, 
                               extra_sentences=extra_sentences, 
                               similarity_percentage=round(similarity_percentage, 2)) 
 
    except Exception as e: 
        flash(f"An error occurred: {str(e)}", 'danger') 
        return redirect(url_for('home')) 
 
if __name__ == "__main__": 
    app.run(host='localhost', port=5000, debug=True)