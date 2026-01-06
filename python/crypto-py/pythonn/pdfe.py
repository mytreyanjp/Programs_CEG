import ollama
from PyPDF2 import PdfReader

# Load the PDF
reader = PdfReader("des.pdf")
text = ""
for page in reader.pages:
    text += page.extract_text()
print(text)
# Ask a question about the content
response = ollama.chat(model='llama2', messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": f"Here is the document:\n{text[:4000]}\n\nSummarize it."}
])

print(response['message']['content'])
