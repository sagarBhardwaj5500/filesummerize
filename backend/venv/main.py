# File: backend/main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import uuid
from transformers import GPT2Tokenizer, GPT2Model

app = FastAPI()

# Set up file storage
UPLOAD_FOLDER = 'uploads'

# Load pre-trained GPT-2 model
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
model = GPT2Model.from_pretrained('gpt2')

class Document(BaseModel):
    file: UploadFile = File(...)

@app.post("/upload")
async def upload_document(document: Document):
    file = document.file
    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    return {"message": "File uploaded successfully"}

@app.post("/summarize")
async def summarize_document(document: Document):
    file = document.file
    filename = file.filename
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    # Load the uploaded file
    with open(file_path, "r") as f:
        text = f.read()
    # Preprocess the text
    inputs = tokenizer.encode_plus(
        text,
        add_special_tokens=True,
        max_length=512,
        return_attention_mask=True,
        return_tensors='pt'
    )
    # Generate summary using GPT-2
    outputs = model.generate(
        inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        max_length=128,
        num_beams=4,
        no_repeat_ngram_size=2,
        early_stopping=True
    )
    # Convert summary to text
    summary = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {"summary": summary}