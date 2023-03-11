import os
import cohere
from dotenv import load_dotenv
from pdftotext import convert_pdf_to_string

load_dotenv()
COHERE_API = os.getenv('COHERE_API')
co = cohere.Client(COHERE_API)
url = 'https://www.law.columbia.edu/sites/default/files/2023-02/Trickle_Down_Feb14%20%281%29.pdf'

text = convert_pdf_to_string(url)

response = co.summarize(
    text=text,
    model='summarize-xlarge',
    length='long',
    format = 'paragraph',
    extractiveness='medium',
    temperature=0.5,
)

summary = response.summary

print(summary)

summary = response.summary