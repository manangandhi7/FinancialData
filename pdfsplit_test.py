__author__ = 'manan'


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


split_pdf_pages('reports/new/Airtel.pdf', 'reports/2016', 'Airtel.pdf', 2)
