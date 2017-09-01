#!/usr/bin/env python
# -*- coding: utf-8 -*-
from nltk.parse.malt import find_malt_model

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
from data_holder.LangModel import *

gram_count = 3

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
    #lst = get_vertical_line(layout, bbox[0], bbox[1], bbox[2], bbox[3])

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


def find_me_box(obj, text):
    x1 = 0.0
    x2 = 0.0
    y1 = 0.0
    y2 = 0.0

    index = 0
    temp_index = 0
    objs = obj._objs

    for i in range(0, len(objs)):
        if isinstance(objs[i], pdfminer.layout.LTChar):
            if objs[i].get_text() == text[index]:
                begin_date = objs[i]
                temp_index = i
                index += 1


def find_financial_year2(layout, bbox):
    lst = get_vertical_line(layout, bbox[0], bbox[1], bbox[2], bbox[3])

    lst2 = []

    for obj in lst:
        text = obj.get_text()
        lst_dates = find_dates(text)
        for item in lst_dates:

            if find_text_in_horizon(obj.bbox[1], obj.bbox[3], layout, 'note'):
                date = item
                print date
                lst2.append(item)

    #if one date is found, perfect
    if len(lst2) == 1:
        return date

    if len(lst2) > 0:

        return date

    #if not, try to find the closest one
    for item in lst:
        text = item.get_text()
        lst_dates = find_dates(text)
        for item in lst_dates:
            if find_text_in_horizon(item.bbox[1], item.bbox[3], layout, 'note'):
                date = item
                print date
                lst2.append(item)
                break

    return lst_dates

#find_date('30   Sep ’ 16 June’ 16 Sep')

regex_profit_before_tax = [
                        'profit before tax',
                        'pre-tax profit/\(loss\)',
                        'Profit/ \(loss\) before tax',
                        'Profit (.*?) before tax'
                        ]

def find_profit_before_tax(obj):
    for line in regex_profit_before_tax:
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

def ngrams(input, n):
  #input = input.split(' ')
  output = []
  for i in range(len(input)-n+1):
    output.append(input[i:i+n])
  return output

def find_sim_ngrams(first, second):
    count = 0
    for item1 in first:
        if item1 in second:
            count += 1
    for item2 in second:
        if item2 not in first:
            count -= 1
    return count

profit_bt_model = LangModel()
profit_bt_model.add_data_from_text('profit loss before EXCEPTIONAL ITEMS AND TAX'.lower())

#first find all the strings
#classify if possible so we have minimum candidates by positions or by other text on the page
#next,

def find_profit_after_tax(layout_list):
    lst_profit_before_tax = []

    candidates_profit_before_tax = []

    # loop over the object list
    for layout in layout_list:
        for obj in layout._objs:
            # if it's a textbox, print text and location
            if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                #if re.search('profit before tax', obj.get_text(), re.IGNORECASE):
                    #lst_profit_before_tax.append(obj)
                #print "%6d, %6d, %s" % (obj.bbox[0], obj.bbox[1], obj.get_text()) #.replace('\n', ''))
                if obj.get_text() == 'Profit before tax (I-II)':
                    print 'ping me'
                for obj2 in obj._objs:
                    #if find_profit_before_tax(obj2):
                        #lst_profit_before_tax.append(obj2)
                    for line in regex_profit_before_tax:
                        if re.search(line, obj.get_text(), re.IGNORECASE):
                            lst_profit_before_tax.append(obj2)
                            #print obj2.get_text()
                        elif re.search('profit', obj.get_text(), re.IGNORECASE) or re.search('before', obj.get_text(), re.IGNORECASE) or re.search('tax', obj.get_text(), re.IGNORECASE):
                            candidates_profit_before_tax.append(obj2)

        #continue
        #if not found, try to find the one with the highest probability:
        max_sim = -100
        max_match_obj = None
        if len(lst_profit_before_tax) == 0:
            for obj2 in candidates_profit_before_tax:
                curr_model = LangModel()
                curr_model.add_data_from_text(obj2.get_text().lower())
                #sim2 = profit_bt_model.get_model_similarity(curr_model)
                #print profit_bt_model.dict.values()
                #print curr_model.dict.values()
                sim2 = profit_bt_model.KL(curr_model)
                if sim2 > max_sim:
                    max_sim = sim2
                    max_match_obj = obj2

        if max_match_obj is not None:
            lst_profit_before_tax.append(max_match_obj)
            print 'CATCH : ' + max_match_obj.get_text()

        for horizontal_box in lst_profit_before_tax:
            '''
            if(horizontal_box.bbox[0] < (layout.bbox[0] + layout.bbox[2])/2):
                print 'left'
            else:
                print 'right'

            if(horizontal_box.bbox[1] < (layout.bbox[1] + layout.bbox[3])/2):
                print 'bottom'
            else:
                print 'top'
            '''

            lst_horizonto = get_horizontal_line(layout, horizontal_box.bbox[0], horizontal_box.bbox[1], horizontal_box.bbox[2], horizontal_box.bbox[3])

            # new_setup, delete if doesnt work
            lst2 = []
            max_height = -1.0
            min_height = 1000.0

            for item in lst_horizonto:
                height = abs(item.bbox[1] - item.bbox[3])
                if height > max_height:
                    max_height = height
                if height < min_height:
                    min_height = height

            for item in lst_horizonto:
                distance = abs(horizontal_box.bbox[1] + horizontal_box.bbox[3] - item.bbox[1] - item.bbox[3])/2
                if distance <= min_height/2:
                    lst2.append(item)

            lst_horizonto = lst2
            # new_setup, delete if doesnt work

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

This are the keyword we are looking for:

"STATEMENT OF PROFIT AND LOSS"

For the year ended 31st March, 2016 (rupees in Crores)

pre-tax profit/(loss)
profit before tax
Profit before Exceptional item & tax
Profit/ (loss) before tax (VII-VIII)
Profit for the year = profit after tax

profit after tax
profit of the year


HSBC, Citigroup, Morgan Stanley say end of market boom is nigh

Breakdown in trading patterns is signal to get out soon

'''
