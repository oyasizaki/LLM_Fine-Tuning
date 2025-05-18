# -*- coding: utf-8 -*-
"""
Created on Apr 27

@author: Oyasi

@app: v0.2

Text book type pdf converter (larger pdf files)
"""




import pdfplumber
import ollama
import json
import os
import re

# Function to extract text from a PDF file while filtering out non-textual content
def extract_text_from_pdf(pdf_file_path):
    text = ''
    with pdfplumber.open(pdf_file_path) as pdf:
        for page in pdf.pages:
            # Extract text
            page_text = page.extract_text()
            text += page_text + '\n'
    return text

# Function to divide text into chunks
def divide_text_into_chunks(text, chunk_size=128):  # Adjust chunk size here
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

# Function to generate question and answer for each chunk using Ollama, with retry mechanism
def generate_qa_for_chunk_with_retry(chunk, max_retries=2):
    retries = 0
    while retries <= max_retries:
        try:
            prompt = "You are an API that converts bodies of text into a single question and answer into a JSON format. Each JSON " \
                     "contains a single question with a single answer. Only respond with the JSON and no additional text. \n"
            response = ollama.chat(model='llama2', messages=[{'role': 'user', 'content': prompt + chunk}])
            if response['message']['content'].strip() == "":
                raise ValueError("Empty response")
            return response['message']['content']
        except Exception as e:
            retries += 1
    print("Reached maximum retries. Skipping this chunk.")
    return None

# Get the PDF file path
pdf_file_path = 'C:\\Users\\Home\\Desktop\\Datasets\\part1.pdf'  # Update with your PDF file path

# Extract text from PDF while filtering out non-textual content
pdf_text = extract_text_from_pdf(pdf_file_path)

# Divide text into smaller chunks
text_chunks = divide_text_into_chunks(pdf_text)

# Process each chunk to generate question and answer, and store them in a list
qa_list = []
for chunk in text_chunks:
    qa = generate_qa_for_chunk_with_retry(chunk)
    if qa is not None:
        # Load JSON data retrieved from Ollama
        try:
            qa_json = json.loads(qa)
            qa_list.append(qa_json)
        except json.JSONDecodeError as e:
            pass  # Ignore JSON decoding errors

# Create directory if it doesn't exist
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save the generated question-answer pairs to a JSON file
output_file_path = os.path.join(output_dir, 'responses.json')
with open(output_file_path, 'w') as f:
    json.dump({"responses": qa_list}, f)
