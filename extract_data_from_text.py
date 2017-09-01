#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'manan'


#import financial_report_analyzer.py
from financial_report_analyzer import *
from extract_stuff import *
import os

for file in os.listdir("reports/2016"):
    if file.endswith(".pdf"):
        try:
            file_path = os.path.join("reports/2016", file)
            layout_list = get_data_from_pdf(file_path)
        except:
            print 'could not process : ' + file
            continue

    #layout contains all the information about the text
    #layout_list = get_data_from_pdf('reports/2016/Balrampur_chini.1.pdf')
    #layout_list = get_data_from_pdf('reports/2016/Emami.1.pdf')
    #layout_list = get_data_from_pdf('tata_motors.pdf')
    #layout_list = get_data_from_pdf('reports/2016/Alembic_pharma.1.pdf')
    #layout_list = get_data_from_pdf('reports/2016/GE_power.1.pdf')
    #layout_list = get_data_from_pdf('reports/2016/Timken_india.1.pdf')
    #layout_list = get_data_from_pdf('reports/2016/Zandu_realty.1.pdf')


    #we care about only 4th page for now
    #layout_list = [layout_list[403]]

    #get all text from dict
    #text = get_all_text_from_layout_list(layout_list)
    #text = text.encode('utf-8')
    #text = text.replace('’', '\'')
    #text = text.replace('\t', ' ')
    #text = text.replace('\r', ' ')
    #text = text.replace('\n', ' ')

    #print text
    #retrieve currency
    #find the frequency of INR, USD, EUR, rupees, euros, dollars. that will tell the currency

    #find_date(text)

    print file
    find_profit_after_tax(layout_list)

    #just the frequency should be enough for the first phase ()


    #different types of dates:
    #dd-mmm-yy, mmm-yy, etc.


    #financial year we are talking about
    #profit before tax
    #profit after tax
    #profit per share
    #in lacs crores (crs.), million,
    #total revenue/turnover
    #dividend
    #segment revenue
    #total taxes
    #charity
    #operations in country
    #liabilities
    #assets
    #company name/scrip
