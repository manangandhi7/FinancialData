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
extensions = 'st|th|rd'
spacers2 = ' |\''
day_spacers =' |\.|\\|/'
month_spacers = ' |\'|,|\.|\\|/'

#print re.findall(re_date1, text, flags=re.IGNORECASE)
#find_date('31st March, 2017')

popular_date_formats = []

#3,02,78 - wrong value
#For the year ended 31st March, 2016 (rupees in Crores)
#2016-17
#March 2017
#2016-2017
space = '[ -]'
popular_date_formats.append('20\d{2}'+ space + '{1,2}' +'\d{4}') #2016-2017

date_part = '(31|30|((1|2)[0-9])|(0?[1-9]))'
month_part = '(11|12|0[1-9]{1})'
year_part = '(\d{4}|\d{2})'

regex = date_part + '(' + spacers2 + ')?' + '(' + extensions + ')?'
regex = regex + '(' + day_spacers + '){1,2}'

date1 = regex + '(' + full_months + '|' + short_months + '|' + month_part + ')' + '(' + month_spacers + '){1,2}'
date1 += year_part
popular_date_formats.append(date1) #dd-mmm/mm-yyyy/yy

date4 = '(' + full_months + '|' + short_months + ')' + '( |\'|-){1,2}'
date4 += date_part + '(' + spacers2 + ')?' + '(' + extensions + ')?'
date4 += '[, \']{1,2}' + year_part
popular_date_formats.append(date4)

date2 = '(' + full_months + '|' + short_months + '|'+ month_part +')' + '(' + month_spacers + '){1,2}'
date2 += '\d{4}'
popular_date_formats.append(date2) #mmm/mm-yyyy

date3 = '(' + full_months + '|' + short_months + ')' + '(' + month_spacers + '){1,2}'
date3 += year_part
popular_date_formats.append(date3) #mmm-yyyy/yy

popular_date_formats.append('20\d{2}'+ space + '{1,2}' +'\d{2}') #2016-17

def find_dates(text):
    #TODO replace [/\'] with - for the dates
    lst_dates = []
    found = True
    while found == True:
        found = False
        for item in popular_date_formats:
            m = re.search(item, text, flags=re.IGNORECASE)
            if m is not None:
                date = m.group(0)
                found = True
                text = text.replace(date, ' ')
                lst_dates.append(date)
                break
    if len(lst_dates) > 0:
        return True
    return False
    #return lst_dates

def find_financial_year(layout, bbox):
    for obj in layout._objs:
        # if it's a textbox, print text and location
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            for obj2 in obj._objs:
                date = None
                text = obj2.get_text()
                lst_dates = find_dates(text)
                for item in lst_dates:
                    if find_text_in_horizon(obj2.bbox[1], obj2.bbox[3], layout, 'note'):
                        date = item
                        print date
                        break
                if date is not None:
                    break
    return lst_dates

#find_date('30   Sep ’ 16 June’ 16 Sep')

lst_profit_before_tax = ['pre-tax profit/\(loss\)',
                        'profit before tax',
                        'Profit/ \(loss\) before tax']
def find_profit_before_tax(obj):
    for line in lst_profit_before_tax:
        #if re.search('before tax', obj.get_text(), re.IGNORECASE):
        #    print obj.get_text()
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
                    #lst = find_financial_year(layout, item.bbox)

                    #go up and find the date
                    lst = get_vertical_line(layout, item.bbox[0], item.bbox[1], item.bbox[2], item.bbox[3])
                    print str(number) + ' : '
                    for item2 in lst:
                        if find_dates(item2.get_text()):
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
                if(fuzzy_veritcal_line_match(x1, x2, obj2.bbox[0], obj2.bbox[2])):
                    lst.append(obj2)
    return lst

def fuzzy_line_match(x1, x2, x1d, x2d):
    if (x1 + x2) * 1.035 > x1d + x2d and (x1 + x2) * 0.965 < x1d + x2d:    #3%? why not 4%? need more data to decide threshold
        return True
    return False

def find_text_in_horizon(y1, y2, layout, text, threshold=1):
    if threshold != 1:
        raise Exception('I don\'t know how to utilize threshold!')
    for obj in layout._objs:
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            for obj2 in obj._objs:
                if(fuzzy_line_match(y1, y2, obj2.bbox[1], obj2.bbox[3])):
                    if re.search(text, obj2.get_text(),flags=re.IGNORECASE):
                        return True
    return False

def fuzzy_veritcal_line_match(x1, x2, x1d, x2d):
    left = -1.0
    right = -1.0
    center = 1000000.0
    if x2 - x1 > x2d - x1d:
        center = (x2d + x1d)/2
        left = x1
        right = x2
    else :
        center = (x1 + x2)/2
        left = x1d
        right = x2d
    #algo1
    '''
    if center > x2d or center < x1d:
        return False
    return True
    '''
    #algo2
    if (x1 <= x1d and x2 > x1d) or (x1 > x1d and x2d > x1 ): #TODO also check for range of at least 50%
        return True
    return False

#TODO use this method before date parsing and other lookups
def preprocess_text(text):
    return remove_spaces(text)

def remove_spaces(text):
    text = text.replace('\t', ' ')
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    while '  ' in text:
        text = text.replace('  ', ' ')
    return text

