#report analyzer using PDF,
#for images within pdf, use Tesseract OCR

'''
import PyPDF2
pdfFileObj = open('reliance.pdf','rb')     #'rb' for read binary mode
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
print (pdfReader.numPages)
pageObj = pdfReader.getPage(9)          #'9' is the page number

print(pageObj.extractText())
'''

from pickle_handler import *
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer

def parse_obj(lt_objs):
    # loop over the object list
    for obj in lt_objs:

        # if it's a textbox, print text and location
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            print "%6d, %6d, %s" % (obj.bbox[0], obj.bbox[1], obj.get_text().replace('\n', '_'))
            #for obj2 in obj._objs:
            #    print obj2._objs

        # if it's a container, recurse
        elif isinstance(obj, pdfminer.layout.LTFigure):
            parse_obj(obj._objs)

def get_data_from_pdf(file_name):
    pkl_file = ''
    temp = file_name
    if len(file_name.split('.')) > 0:
        #splits = file_name.split('.')
        #pkl_file = file_name.replace('.' + splits[len(splits) - 1], 'pkl')
        pkl_file = temp.replace('.pdf', '.pkl')
        layout_list = read_pickle(pkl_file)
        if layout_list is not None:
            return layout_list


    # Open a PDF file.
    fp = open(file_name, 'rb')

    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)

    # Create a PDF document object that stores the document structure.
    # Password for initialization as 2nd parameter
    document = PDFDocument(parser)

    # Check if the document allows text extraction. If not, abort.
    #if not document.is_extractable:
    #    raise PDFTextExtractionNotAllowed

    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()

    # Create a PDF device object.
    device = PDFDevice(rsrcmgr)

    # BEGIN LAYOUT ANALYSIS
    # Set parameters for analysis.
    laparams = LAParams()

    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)

    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    layout_list = []

    # loop over all pages in the document
    for page in PDFPage.create_pages(document):
        try:
            # read the page into a layout object
            interpreter.process_page(page)
            layout = device.get_result()
            layout_list.append(layout)
        except:
            print 'Could not extract page : ' + str(len (layout_list) + 1) + ' in file : ' + file_name

        # extract text from this object
        #parse_obj(layout._objs)

    if pkl_file != '':
        write_pickle(pkl_file, layout_list)
    return layout_list

def get_pdf_list_from_file(file_name):
    # Open a PDF file.
    fp = open(file_name, 'rb')

    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)

    # Create a PDF document object that stores the document structure.
    # Password for initialization as 2nd parameter
    document = PDFDocument(parser)

    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed
    #OR: just return None may be??

    # loop over all pages in the document
    return PDFPage.create_pages(document)

def get_all_text_from_single_layout(layout):
    text = ''
    for obj in layout._objs:
        # if it's a textbox, print text and location
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            text += obj.get_text().replace('\n', ' ')
    return text

def get_all_text_from_layout_list(layout_list):
    text = ''
    for layout in layout_list:
        # loop over the object list
        for obj in layout._objs:

            # if it's a textbox, print text and location
            if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                text += obj.get_text().replace('\n', ' ')
                #for obj2 in obj._objs:
                #    print obj2._objs

            # if it's a container, recurse
            #elif isinstance(obj, pdfminer.layout.LTFigure):
            #    parse_obj(obj._objs)
    return text
