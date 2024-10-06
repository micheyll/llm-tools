import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize
import requests
import sys
import signal
import os
import time

def signal_handler(sig, frame):
    print('\nScript interrupted. Partial results have been saved.')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def wait_for_model_readiness(ollama_url, model_name, max_retries=30, retry_interval=10):
    print(f"Checking if model '{model_name}' is loaded and ready...")
    for attempt in range(max_retries):
        try:
            # First, check if the model is listed
            response = requests.get(f"{ollama_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get('models', [])
                if not any(model['name'] == model_name for model in models):
                    print(f"Model '{model_name}' not found. Retrying in {retry_interval} seconds...")
                    time.sleep(retry_interval)
                    continue

            # If the model is listed, try to generate a simple response
            test_prompt = "Hello, are you ready?"
            response = requests.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": model_name,
                    "prompt": test_prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"Model '{model_name}' is loaded and ready.")
                return True
            else:
                print(f"Model not fully ready. Status: {response.status_code}. Retrying in {retry_interval} seconds...")
        except requests.exceptions.RequestException as e:
            print(f"Error checking model status: {e}")
        
        time.sleep(retry_interval)
    
    print(f"Model '{model_name}' not ready after {max_retries} attempts. Exiting.")
    return False

def extract_text_from_epub(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters

def clean_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()

def chunk_text(text, chunk_size=5000):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def process_chunk_with_llm(chunk, ollama_url, model_name):
    prompt = f"Extract biographical information about Audrey Hepburn from this text, focusing on factual details that are interesting to someone wanting to know everything about Audrey. Do not add your own commentary, just give the facts. Use full sentences. The text is as follows: \
            {chunk}"
    
    try:
        print(f"Sending request to Ollama at {ollama_url}")
        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False
            },
            timeout=30
        )
        
        print(f"Received response from Ollama. Status code: {response.status_code}")
        print(f"Response content: {response.text[:500]}...")  # Print first 500 characters of response
        
        response.raise_for_status()
        return response.json()['response']
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Ollama: {e}")
        return None

def main(epub_path, ollama_url="http://llm.anime.world:11434", model_name="command-r:latest"):
    if not wait_for_model_readiness(ollama_url, model_name):
        return

    chapters = extract_text_from_epub(epub_path)
    all_text = " ".join([clean_html(chapter) for chapter in chapters])
    chunks = chunk_text(all_text)
    
    output_filename = "audrey_hepburn_bio.txt"
    
    with open(output_filename, "w") as f:
        for i, chunk in enumerate(chunks):
            print(f"Processing chunk {i+1}/{len(chunks)}...")
            print(chunk[:500] + "...")  # Print first 500 characters of the chunk
            info = process_chunk_with_llm(chunk, ollama_url, model_name)
            if info:
                print(f"Received information from LLM for chunk {i+1}")
                f.write(info + "\n\n")  # Write each chunk's result immediately
                f.flush()  # Ensure it's written to disk
            else:
                print(f"Warning: No information extracted from chunk {i+1}")
    
    print(f"Processing complete. Output saved to: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    main("hepburn.epub")
