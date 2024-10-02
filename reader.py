import pdfreader
from pdfreader import PDFDocument, SimplePDFViewer

from io import BytesIO
with open("sample.pdf", "rb") as f:
    stream = BytesIO(f.read())
doc2 = PDFDocument(stream)

print(doc2)

all_pages = [p for p in doc2.pages()]

print(len(all_pages))