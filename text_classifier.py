#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'manan'

from nltk import tokenize
from financial_report_analyzer import *
from extract_stuff import *
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer

from data_holder.LangModel import LangModel
import os

def custom_pdf_processor_for_classification(pdf_pages):
    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()

    # BEGIN LAYOUT ANALYSIS
    # Set parameters for analysis.
    laparams = LAParams()

    # Create a PDF page aggregator object.
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)

    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    layout_list = []
    # loop over all pages in the document

    for page in pdf_pages:


        # read the page into a layout object
        interpreter.process_page(page)
        layout = device.get_result()
        layout_list.append(layout)

        # extract text from this object
        #parse_obj(layout._objs)

    return layout_list


porter = PorterStemmer()
snowball = SnowballStemmer('english')
wordnet = WordNetLemmatizer()

lang_model = LangModel()
lang_model.create_model_from_fixed_list()

must_have_words = ['profit',
                   'loss',
                   'statement',
                   'summary',
                   'statement',
                   'revenue',
                   'cost',
                   'before',
                   'after',
                   'Consolidated',
                   'income',
                   'earning',
                   'expense',
                   'basic',
                   'diluted',
                   'revenue',
                   'operati',
                   'exceptional'
                   'tax'
                ]

'''

thought experiment:

lightning network:

government creates coins:

users get it through salary and stuff

users can spend it because they know the value (in god we trust)

the problem with cryptos is: it needs a central ledger.
what if you can create a currency which has a wallet with your own coins

coin client:
signed packet from an authority
'''

import PyPDF2


def split_pdf_pages(input_pdf_path, target_dir, file_name, page_num, fname_fmt=u"{num_page:04d}.pdf"):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    with open(input_pdf_path, "rb") as input_stream:
        input_pdf = PyPDF2.PdfFileReader(input_stream)

        if input_pdf.flattenedPages is None:
            # flatten the file using getNumPages()
            input_pdf.getNumPages()  # or call input_pdf._flatten()

        #for num_page, page in enumerate(input_pdf.flattenedPages):
        if True:
            output = PyPDF2.PdfFileWriter()
            #output.addPage(page)
            output.addPage(input_pdf.getPage(page_num))

            file_name = os.path.join(target_dir, file_name + '.' + fname_fmt.format(num_page=page_num))
            with open(file_name, "wb") as output_stream:
                output.write(output_stream)

#layout contains all the information about the text
#layout_list = get_data_from_pdf('reports/new/DLF.pdf')
#layout_list = get_data_from_pdf('reports/new/Guj_Coke.pdf')
#layout_list = get_data_from_pdf('reports/new/Zandu_realty.pdf')
#layout_list = get_data_from_pdf('reports/2016/Emami.1.pdf')
#layout_list = get_data_from_pdf('tata_motors.pdf')
#layout_list = get_data_from_pdf('reports/2016/Alembic_pharma.1.pdf')
#layout_list = get_data_from_pdf('reports/2016/GE_power.1.pdf')
#layout_list = get_data_from_pdf('reports/2016/Timken_india.1.pdf')
#layout_list = get_data_from_pdf('reports/2016/Zandu_realty.1.pdf')
debug = ''

for file in os.listdir("reports/alll"):
    if file.endswith(".pdf"):
        try:
            file_path = os.path.join("reports/alll", file)
            layout_list = get_data_from_pdf(file_path)
        except:
            print 'could not process : ' + file
            continue

    #get all text from dict
    #text = get_all_text_from_layout_list(layout_list)
    #text = text.encode('utf-8')
    #text = text.replace('’', '\'')
    #text = text.replace('\t', ' ')
    #text = text.replace('\r', ' ')
    #text = text.replace('\n', ' ')

#if True:
    #layout_list = get_data_from_pdf('reports/new/Symphony.pdf')
    max_sim = 0.0
    max_lang_model = None
    max_text = ''
    max_page = 0
    num = 0
    #debug += '\n\n\n' + file + '\n\n'
    for layout in layout_list:
        num += 1
        text = get_all_text_from_single_layout(layout)
        count = 0
        for item in must_have_words:
            if re.search(item, text, flags=re.IGNORECASE):
                count += 1
        if count < 8: #this has nothing to do with the model, just an optimization step
            continue
        temp_lang_model = LangModel()
        temp_lang_model.add_data_from_text(text)
        sim2 = lang_model.get_model_similarity(temp_lang_model)
        debug += 'page : ' + str(num) + ' similarity : ' + str(sim2) + '\n'
        if sim2 > max_sim:
            max_sim = sim2
            #max_lang_model = temp_lang_model
            max_page = num
            #max_text = text

    #print max_sim
    #print max_text
    #print max_page
    if max_page > 0:
        split_pdf_pages(file_path, 'reports/2016', file.replace('.pdf', ''), max_page - 1)
    print file + ' : max_page : ' + str(max_page)

file2 = open('output.txt', 'w+')
file2.write(debug)
file2.close()

'''
print 'max model \n\n'

for item in max_lang_model.dict.keys():
    print item + ' : ' + str(max_lang_model.dict[item])

print 'orig model \n\n'

for item in lang_model.dict.keys():
    print item + ' : ' + str(lang_model.dict[item])
#print lang_model.dict

'''
