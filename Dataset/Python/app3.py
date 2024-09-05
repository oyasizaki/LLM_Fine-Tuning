# -*- coding: utf-8 -*-
"""
Created on Apr 26

@author: Oyasi

@app: v0.1.3

Simple document(pdf) converter - sentence based chunk size
"""



import PyPDF2
import ollama
import json
import os
import nltk

# Download NLTK punkt tokenizer data
nltk.download('punkt')

# Function to extract text from a PDF file
def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as pdf_file_obj:
        pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page_obj = pdf_reader.pages[page_num]
            text += page_obj.extract_text()
    return text

# Function to divide text into sentence-level chunks
def divide_text_into_sentence_chunks(text):
    sentences = nltk.sent_tokenize(text)
    return sentences

# Function to process text chunks using Ollama
def process_text_chunks(sentences, prompt):
    responses = []
    for sentence in sentences:
        response = ollama.chat(
            model='llama2',
            messages=[{'role': 'user', 'content': prompt + sentence}],
        )
        responses.append(response)
    return responses

# Define the PDF file path
pdf_file_path = 'C:\\Users\\Oyasi\\Desktop\\Project\\Dataset\\srt.pdf'  # Update with your PDF file path

# Define the command/prompt
prompt = "You are an API that converts bodies of text into a single question and answer into a JSON format. Each JSON " \
          "contains a single question with a single answer. Only respond with the JSON and no additional text. \n"

# Extract text from PDF
pdf_text = extract_text_from_pdf(pdf_file_path)

# Divide text into sentence-level chunks
sentences = divide_text_into_sentence_chunks(pdf_text)

# Process text chunks using Ollama
responses = process_text_chunks(sentences, prompt)

# Create directory if it doesn't exist
output_dir = 'output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Save responses to a JSON file
output_file_path = os.path.join(output_dir, 'responses.json')
with open(output_file_path, 'w') as f:
    json.dump(responses, f)

print(f"Responses saved to {output_file_path}")
