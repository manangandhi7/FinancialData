#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'manan'
import re

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

full_months = 'january|february|march|april|may|june|july|august|september|october|november|december'
short_months = 'jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec'
#dates = '1st|2nd|3rd|4th|5th|6th|7th|8th|9th|10th|11th|12th|13th|14th|15th|16th|17th|18th|19th|20th|21st|22nd|23rd|24th|25th|26th|27th|28th|29th|30th|31st'
extensions = 'st|th|rd'



def regex_match(text, regex):
    print 'nothing'

def find_date(text):
    #result = re.match(pattern, string)
    date_part = '(\d{1,2}\\t*\\n*\\r*[/ -])?'
    date_part = '((30|31|((1|2)[0-9])|(0?[1-9]))\\t*\\n*\\r*[\\/ -])?'
    month_part = '(' + full_months + '|'+ short_months+'|\d{2})\\t*\\n*\\r*[\'/ -]'
    year_part = '\\t*\\n*\\r*(\d{4}|\d{2})'
    re_date1 = date_part + '\\t*\\n*\\r*' + month_part + '\\t*\\n*\\r*' +  year_part

    #\d{1,2}([ \t\r\n]{0,2}(st|th|nd)) = 1 st

    '''m = re.search(re_date1, text)
    if m is not None:
        print m.group(0)
    m = re.search('(' + full_months + '|' + short_months + ')', text)
    if m is not None:
        print m.group(0)
    '''
    #re_date1 = full_months + '|' + short_months + '|\d{2}[/ -]'
    print re_date1
    print re.findall(re_date1, text, flags=re.IGNORECASE)
    #for item in m:
     #   print str(m)

def find_date_in_headers(text):
    #For the year ended 31st March, 2016 (rupees in Crores)
    #2016-2017
    #March 2017

    #2016-2017
    space = '[\\t\'/ -]'
    if re.match('20\d{2}'+ space + '{0,2}' +'\d{4}', text):
        return True
    #2016-17
    if re.match('20\d{2}'+ space + '{0,2}' +'\d{2}', text):
        return True
    return False
    #result = re.match(pattern, string)
    date_part = '(\d{1,2}\\t*\\n*\\r*[/ -])?'
    date_part = '((30|31|((1|2)[0-9])|(0?[1-9]))\\t*\\n*\\r*[\\/ -])?'
    month_part = '(' + full_months + '|'+ short_months+'|\d{2})\\t*\\n*\\r*[\'/ -]'
    year_part = '\\t*\\n*\\r*(\d{4}|\d{2})'
    re_date1 = date_part + '\\t*\\n*\\r*' + month_part + '\\t*\\n*\\r*' +  year_part

    #\d{1,2}([ \t\r\n]{0,2}(st|th|nd)) = 1 st

    '''m = re.search(re_date1, text)
    if m is not None:
        print m.group(0)
    m = re.search('(' + full_months + '|' + short_months + ')', text)
    if m is not None:
        print m.group(0)
    '''
    #re_date1 = full_months + '|' + short_months + '|\d{2}[/ -]'
    print re_date1
    print re.findall(re_date1, text, flags=re.IGNORECASE)
    #for item in m:
     #   print str(m)

#find_date('30   Sep ’ 16 June’ 16 Sep')

'''


find_date('30 sep\'16')
find_date('01-06\'2017')
find_date('01-june-2017')
find_date('1-june-2017')
find_date('01 june 2017')
find_date('01/06/2017')
find_date('01 06 2017')
find_date('06 jun 2017')
find_date('06 jun 17')
find_date('01 06 17')
find_date('june 17')
find_date('2017 - 18')
find_date('Jun 17 - May 18')


This is the keyword we are looking for:

"STATEMENT OF PROFIT AND LOSS"


separator [-' ]
19dd-dd
20dd-dd
dd-dd
mm' yy
mm' yyyy
mmm' yyyy
mmm' yy

For the year ended 31st March, 2016 (rupees in Crores)
2016-2017
March 2017


pre-tax profit/(loss)
profit before tax
Profit/ (loss) before tax (VII-VIII)

profit after tax
profit of the year




'''


lst_profit_before_tax = ['pre-tax profit/\(loss\)',
                        'profit before tax',
                        'Profit/ \(loss\) before tax']
def find_profit_before_tax(obj):
    for line in lst_profit_before_tax:
        if re.search(line, obj.get_text(), re.IGNORECASE):
            return True
    return False

def get_number_from_string(text):
    lst = ['(', ')', ',', '\'', '-']
    for str in lst:
        text = text.replace(str, '')
    return text

#first find all the strings
#classify if possible so we have minimum candidates by positions or by other text on the page
#next,

def find_profit_after_tax(layout_list):
    lst_profit_before_tax = []

    # loop over the object list
    for layout in layout_list:
        for obj in layout._objs:

            # if it's a textbox, print text and location
            if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                #if re.search('profit before tax', obj.get_text(), re.IGNORECASE):
                    #lst_profit_before_tax.append(obj)
                #print "%6d, %6d, %s" % (obj.bbox[0], obj.bbox[1], obj.get_text()) #.replace('\n', ''))
                for obj2 in obj._objs:
                    if find_profit_before_tax(obj2):
                        lst_profit_before_tax.append(obj2)

        for horizontal_box in lst_profit_before_tax:
            if(horizontal_box.bbox[0] < (layout.bbox[0] + layout.bbox[2])/2):
                print 'left'
            else:
                print 'right'

            if(horizontal_box.bbox[1] < (layout.bbox[1] + layout.bbox[3])/2):
                print 'bottom'
            else:
                print 'top'

            lst_horizonto = get_horizontal_line(layout, horizontal_box.bbox[0], horizontal_box.bbox[1], horizontal_box.bbox[2], horizontal_box.bbox[3])
            print horizontal_box.get_text()
            for item in lst_horizonto:
                if item.bbox[0] <= horizontal_box.bbox[0]:
                    continue
                try:
                    number = float(get_number_from_string(item.get_text()))
                    #go up and find the date
                    lst = get_vertical_line(layout, item.bbox[0], item.bbox[1], item.bbox[2], item.bbox[3])
                    print str(number) + ' : '
                    for item2 in lst:
                        if find_date_in_headers(item2.get_text()):
                        #if re.match('\d{4}-\d{4}', item2.get_text()):
                            print str(number) + ' : ' + item2.get_text()
                except:
                    continue

            # if it's a container, recurse
            #elif isinstance(obj, pdfminer.layout.LTFigure):
                #parse_obj(obj._objs)

def get_horizontal_line(layout, x1, y1, x2, y2):
    lst = []
    for obj in layout._objs:
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            #if re.search('profit before tax', obj.get_text(), re.IGNORECASE):
                #lst_profit_before_tax.append(obj)
            #print "%6d, %6d, %s" % (obj.bbox[0], obj.bbox[1], obj.get_text()) #.replace('\n', ''))
            for obj2 in obj._objs:
                if fuzzy_line_match(y1, y2, obj2.bbox[1], obj2.bbox[3]):
                    lst.append(obj2)
    return lst

def get_vertical_line(layout, x1, y1, x2, y2):
    lst = []
    for obj in layout._objs:
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            #if re.search('profit before tax', obj.get_text(), re.IGNORECASE):
                #lst_profit_before_tax.append(obj)
            #print "%6d, %6d, %s" % (obj.bbox[0], obj.bbox[1], obj.get_text()) #.replace('\n', ''))
            for obj2 in obj._objs:
                if(fuzzy_line_match(x1, x2, obj2.bbox[0], obj2.bbox[2])):
                    lst.append(obj2)
    return lst

def fuzzy_line_match(x1, x2, x1d, x2d):
    if x1 + x2 * 1.035 > x1d + x2d and x1 + x2 * 0.965 < x1d + x2d:    #3%? why not 4%? need more data to decide threshold
        return True
    return False


'''
NEXT TASKS:

Create training and test set:
    get all the reports in one folder
    manually fill their values in a csv

find all the possible dates:
    also, create a library for that?

create a module for comparing results:
    accuracy
    anything else?


'''
