# -*- coding: utf-8 -*-
"""
Created on Apr 26

@author: Oyasi

@app: v0.1.2

Simple document(pdf) converter - smaller chunk size
"""



import PyPDF2
import ollama
import json
import os

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file_path):
    pdf_file_obj = open(pdf_file_path, 'rb')
    pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page_obj = pdf_reader.pages[page_num]
        text += page_obj.extract_text()
    pdf_file_obj.close()
    return text

# Function to divide text into chunks
def divide_text_into_chunks(text, chunk_size=128):  # Adjust chunk size here
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

# Function to generate question and answer for each chunk using Ollama
def generate_qa_for_chunk(chunk):
    prompt = "You are an API that converts bodies of text into a single question and answer into a JSON format. Each JSON " \
             "contains a single question with a single answer. Only respond with the JSON and no additional text. \n"
    response = ollama.chat(model='llama2', messages=[{'role': 'user', 'content': prompt + chunk}])
    return response['message']['content']

# Get the PDF file path
pdf_file_path = 'C:\\Users\\Oyasi\\Desktop\\Project\\Dataset\\srt.pdf'  # Update with your PDF file path

# Extract text from PDF
pdf_text = extract_text_from_pdf(pdf_file_path)

# Divide text into smaller chunks
text_chunks = divide_text_into_chunks(pdf_text)

# Process each chunk to generate question and answer, and store them in a list
qa_list = []
for chunk in text_chunks:
    qa = generate_qa_for_chunk(chunk)
    qa_list.append(json.loads(qa))

# Create directory if it doesn't exist
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the generated question-answer pairs to a JSON file
output_file_path = os.path.join(output_dir, 'responses.json')
with open(output_file_path, 'w') as f:
    json.dump({"responses": qa_list}, f)

print(f"Responses saved to {output_file_path}")
