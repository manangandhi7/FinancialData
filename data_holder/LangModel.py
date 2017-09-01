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
import os
import csv
import numpy as np
import math

class LangModel:
    def __init__(self):
        self.dict = {}
        self.number_of_shares = 0.0
        self.model_done = False
        self.count = 0.0

    def get_model_data(self):
        return self.dict

    def get_model_similarity(self, model):
        sim = 0.0

        if not self.model_done:
            self.calc_self_probability()
        if not model.model_done:
            model.calc_self_probability()

        for key in self.dict.keys():
            if key in model.dict.keys():
                sim += self.dict[key] * model.dict[key]
            elif model.count > 0:
                sim -=  self.dict[key] * 1/model.count
        return sim

    def KL(self, other_model):
        sim = 0.0

        abc = set()
        dict1 = {}
        dict2 = {}
        dict1_sum = 0
        dict2_sum = 0
        for key in self.dict.keys():
            abc.add(key)
            dict1[key] = self.dict[key]
            dict1_sum += self.dict[key]

        for key in other_model.dict.keys():
            abc.add(key)
            dict2[key] = other_model.dict[key]
            dict2_sum += other_model.dict[key]


        smoother = 0.1
        for key in abc:
            if key not in self.dict.keys():
                dict1[key] = smoother
                dict1_sum += smoother
            if key not in other_model.dict.keys():
                dict2[key] = smoother
                dict2_sum += smoother

        kld_pq = 0.0
        kld_qp = 0.0
        for key in abc:
            kld_pq += dict1[key]/dict1_sum * math.log((dict1[key] /dict1_sum) / (dict2[key]/dict2_sum))
            kld_qp += dict2[key]/dict2_sum * math.log((dict2[key] /dict2_sum) / (dict1[key]/dict1_sum))
        return (kld_pq + kld_qp) / 2

    def get_model_similarity2(self, model):
        sim = 0.0

        if not self.model_done:
            self.calc_self_probability()
        if not model.model_done:
            model.calc_self_probability()

        for key in self.dict.keys():
            if key in model.dict.keys():
                sim += self.dict[key] * model.dict[key]
            elif model.count > 0:
                sim -=  self.dict[key] / model.count

        for key in model.dict.keys():
             if key not in self.dict.keys():
                sim -= model.dict[key] #/ self.count
        return sim

    def calc_self_probability(self):
        if self.model_done:
            return

        for key in self.dict.keys():
            self.dict[key] = self.dict[key] / self.count
        self.model_done = True

    def create_fake_model(self):
        self.model_done = False
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..\play_data\TCS.csv'), 'r') as f:
            self.history_data = [row for row in csv.reader(f) if row[0] != '']
        #print 'new sec initialized!'

    def add_dict_to_model(self, words):
        self.model_done = False
        for word in words:
            self.count += 1
            if word in self.dict:
                self.dict[word]+= 1.0
            else:
                self.dict[word] = 1.0
        #print self.dict

    def add_data_from_layout(self, layout):
        #get all text from dict
        text = get_all_text_from_single_layout(layout)
        clean_words = tokenize_shit(text)
        self.add_dict_to_model(clean_words)

    def add_data_from_text(self, text):
        clean_words = tokenize_shit(text)
        self.add_dict_to_model(clean_words)

    def add_data_from_filename(self, file_name):
        layout_list = get_data_from_pdf(file_name)

        #get all text from dict
        text = get_all_text_from_layout_list(layout_list)

        #print text
        clean_words = tokenize_shit(text)

        self.add_dict_to_model(clean_words)

    def create_model_from_fixed_list(self):
        list = ['reports/2016/Alembic_pharma.0103.pdf',
        'reports/2016/Emami.1.pdf',
        'reports/2016/tata_motors.pdf',
        'reports/2016/GE_power.1.pdf',
        'reports/2016/Timken_india.1.pdf',
        'reports/2016/Zandu_realty.1.pdf']

        for item in list:
            self.add_data_from_filename(item)

def tokenize_shit(text):
    text = text.encode('utf-8')

    porter = PorterStemmer()
    snowball = SnowballStemmer('english')
    wordnet = WordNetLemmatizer()

    #lines_list = tokenize.sent_tokenize(text)
    #sentences.extend(lines_list)

    #words =  tokenize.word_tokenize(text)

    tokenizer = RegexpTokenizer(r'\w+')
    words = tokenizer.tokenize(text)

    clean_words = []
    for word in words:
        if len(word) < 3:
            #print word
            continue
        elif re.match('^\d+$', word):
            #  print word
            continue
        elif word in stopwords.words('english'):
            continue
        else:
            try:
                clean_words.append(porter.stem(word))
            except:
                i = 10

    return clean_words



if __name__ == '__main__':
    langModel = LangModel()
    langModel.create_model_from_fixed_list()
    print(langModel.get_model_data())

