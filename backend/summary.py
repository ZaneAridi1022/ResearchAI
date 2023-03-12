import os
import cohere
from dotenv import load_dotenv
from pdftotext import convert_pdf_to_string
from chatgpt import generate

load_dotenv()
COHERE_API = os.getenv('COHERE_API')
co = cohere.Client(COHERE_API)

def summarize_text(url):
    text = convert_pdf_to_string(url)
    response = co.summarize(
        text=text,
        model='summarize-xlarge',
        length='long',
        format='paragraph',
        extractiveness='medium',
        temperature=0.5,
        additional_command="in third person pov"
    )
    return response.summary

