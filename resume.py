import streamlit as st
import openai
from transformers import pipeline
from PyPDF2 import PdfReader
import docx
from PIL import Image
import pytesseract
import io
import re
from pdf2image import convert_from_bytes  # Import for handling scanned PDFs

# Helper function to replace gender-specific pronouns
def replace_gender_pronouns(text):
    text = re.sub(r'\bhe\b', 'The candidate', text, flags=re.IGNORECASE)
    text = re.sub(r'\bshe\b', 'The candidate', text, flags=re.IGNORECASE)
    text = re.sub(r'\bhim\b', 'The candidate', text, flags=re.IGNORECASE)
    text = re.sub(r'\bher\b', 'The candidate', text, flags=re.IGNORECASE)
    text = re.sub(r'\bhis\b', "The candidate's", text, flags=re.IGNORECASE)
    text = re.sub(r'\bher\'s\b', "The candidate's", text, flags=re.IGNORECASE)
    return text

# Load a summarization model
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

# Summarization using Together API
def summarize_text(query):
    openai.api_base = "https://api.together.xyz/v1"
    openai.api_key = "5edfd827b6a402f0765a7a330cf95c8a43f0f47b484bbc4340bb45204f0d0375"
    response = openai.ChatCompletion.create(
        model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
        messages=[{"role": "system", "content": "Summarize the resume concisely"},
                  {"role": "user", "content": query}]
    )
    return response["choices"][0]["message"]["content"]

# Helper function to extract text from uploaded files
def extract_text(uploaded_file):
    text = ""

    file_name = uploaded_file.name.lower()  # Get file name to check format
    file_bytes = uploaded_file.read()  # Read the file content as bytes
    file_stream = io.BytesIO(file_bytes)  # Convert to a file-like object

    if file_name.endswith(".pdf"):
        reader = PdfReader(file_stream)
        extracted_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        
        if extracted_text.strip():  
            return extracted_text  # Return extracted text if available
        
        # If no extractable text, perform OCR
        images = convert_from_bytes(file_bytes)
        for img in images:
            text += pytesseract.image_to_string(img, lang="eng") + "\n"

        return text if text.strip() else "OCR failed to extract text."

    elif file_name.endswith(".docx"):
        doc = docx.Document(file_stream)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])

    elif file_name.endswith(".txt"):
        return file_bytes.decode("utf-8")

    elif file_name.endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")):
        image = Image.open(file_stream)
        return pytesseract.image_to_string(image, lang="eng")

    else:
        return "Unsupported file type."

# Streamlit app
def main():
    st.title("Resume Summarizer")
    st.write("Upload your resume (PDF, Word, Text, or Image), and get a summarized version.")

    uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt", "png", "jpg", "jpeg"])

    if uploaded_file:
        text = extract_text(uploaded_file)
        if not text or text.strip() == "OCR failed to extract text.":
            st.error("Could not extract text from the uploaded file. Please try again.")
            return

        st.subheader("Extracted Text")
        st.text_area("Full Text", text, height=300)

        with st.spinner("Summarizing..."):
            summary = summarize_text(text)
            summary = replace_gender_pronouns(summary)

        st.subheader("Summary")
        st.write(summary)

if __name__ == "__main__":
    main()
