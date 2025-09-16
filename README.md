# 📝 Text Analysis for Transcription Error (Medical Reports)

This project provides an easy way to **detect transcription errors in medical records** by comparing an original report with a transcribed version. It works for text, PDF, and image files, using OCR for image inputs. The app highlights **differences in drug names and sentences** between the two documents and computes a similarity percentage.  
Additionally, it includes a machine learning workflow to predict medical conditions based on provided medicines.

---

## Project Description

**Text Analysis for Transcription Error** is a web-based tool built with Flask. It allows users to upload or paste their original and transcribed medical reports, and instantly detects:

- **Missing or extra drug names**
- **Missing or extra sentences**
- **Similarity percentage** (based on drug names)

It supports multiple file types:
- **Text**
- **PDF** (using `PyPDF2`)
- **Images** (`.png`, `.jpg`, etc., using Tesseract OCR)

The app also provides a machine learning pipeline to predict **medical conditions** given a list of medicines. This workflow uses TF-IDF with logistic regression and lets you train and save your own models from a CSV database of medicines and conditions.

---

## Features

- Upload or paste original and transcribed content (Text, PDF, Image)
- Compares drug names using regular expressions
- Compares sentences to identify missing/extra content
- Displays a similarity percentage with a visual Bootstrap progress bar
- Handles file uploads securely
- Flash messages for error handling and user feedback
- ML pipeline for medicine→condition prediction (train and inference scripts included)

---

## Project Structure

.
├── app.py # Main Flask web app
├── templates/
│ ├── home.html # User input page
│ ├── away.html # Results page
├── static/uploads/ # Directory for uploaded files
├── medicine_model.py # ML model training and prediction pipeline
├── requirements.txt # Dependency list (Flask, scikit-learn, etc.)
└── README.md

---

## Installation & Setup

1. **Clone the repository**  
git clone https://github.com/your-username/transcription-error-analysis.git
cd transcription-error-analysis



2. **Create a virtual environment and install dependencies**  
python -m venv venv
source venv/bin/activate # On Unix/Mac
venv\Scripts\activate # On Windows
pip install -r requirements.txt



3. **Install Tesseract OCR (required for image inputs):**  
- **On Ubuntu:**  
  ```
  sudo apt install tesseract-ocr
  ```
- **On Windows:**  
  Download and install from [Tesseract OCR releases](https://github.com/tesseract-ocr/tesseract).

4. **Run the Flask app**  
python app.py



5. **Open your browser** at  
http://localhost:5000



---

## Usage

1. Enter or upload your **Original Report** (text, pdf, or image).
2. Enter or upload your **Transcribed Report**.
3. Click **Analyze**.
4. View the results:
- Drug name differences (missing/extra)
- Sentence differences (missing/extra)
- Similarity percentage visualized
- Option to analyze again

---

## Machine Learning Workflow

Train and use a model to predict conditions from medicines:

1. **Preparing Data:**  
Use a CSV with columns:  
- `Condition`  
- `Medicine Names` (comma-separated string)

2. **Training:**  
The class `DrugModelTrainer` (in `medicine_model.py`) loads your CSV, processes medicine lists, and trains a logistic regression model using TF-IDF features.

Example usage:
trainer = DrugModelTrainer("path/to/medicine_name.csv")
trainer.train_and_save()



3. **Prediction:**  
The `DrugModelPredictor` class uses the trained model and vectorizer to predict the condition for new lists of medicines.

Example:
predictor = DrugModelPredictor()
test_meds = ["Paracetamol", "Ibuprofen"]
condition = predictor.predict_condition(test_meds)
print(f"Predicted Condition: {condition}")

text

---

## Requirements

- Python 3.8+
- Flask
- scikit-learn
- pandas
- pytesseract
- pillow
- PyPDF2
- joblib
- Bootstrap (via CDN in HTML)

Install via:
pip install flask scikit-learn pandas pytesseract pillow PyPDF2 joblib



---

## Contributing

Feel free to open issues, questions, or pull requests for improvements.

---

## License

This project is open source and available under the MIT license.
