import pdfminer

import PyPDF2
pdfFileObj = open('reliance.pdf','rb')     #'rb' for read binary mode
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
print (pdfReader.numPages)
pageObj = pdfReader.getPage(9)          #'9' is the page number

print(pageObj.extractText())