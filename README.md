# Resume Summarizer App

## Overview
This is a simple web application built using **Streamlit** that extracts text from a PDF resume and generates a summarized version using a pre-trained NLP model.

## Features
- Upload a **PDF resume**
- Extract text from the resume
- Generate a concise **summary** of the extracted text

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/resume-summarizer.git
   cd resume-summarizer
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the Streamlit app:
```bash
streamlit run app.py
```

## Requirements
openai==0.28.0
pdf2image==1.17.0
Pillow==11.1.0
PyPDF2==3.0.1
pytesseract==0.3.13
python_docx==1.1.2
streamlit==1.41.1
transformers==4.48.2


## Contributing
Feel free to fork this repository and submit a pull request.

## License
This project is licensed under the MIT License.
