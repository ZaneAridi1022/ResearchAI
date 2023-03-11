import io
import requests
import PyPDF2
def convert_pdf_to_string(url):
    r = requests.get(url)
    f = io.BytesIO(r.content)
    reader = PyPDF2.PdfReader(f)
    content = ""
    for page in reader.pages:
        content += page.extract_text()
    return content