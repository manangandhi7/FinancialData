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
        clean_words = self.tokenize_shit(text)
        self.add_dict_to_model(clean_words)

    def tokenize_shit(self, text):
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

    def add_data_from_filename(self, file_name):
        layout_list = get_data_from_pdf(file_name)

        #get all text from dict
        text = get_all_text_from_layout_list(layout_list)

        #print text
        clean_words = self.tokenize_shit(text)

        self.add_dict_to_model(clean_words)

    def create_model_from_fixed_list(self):
        list = ['reports/2016/Alembic_pharma.1.pdf',
        'reports/2016/Emami.1.pdf',
        'tata_motors.pdf',
        'reports/2016/Alembic_pharma.1.pdf',
        'reports/2016/GE_power.1.pdf',
        'reports/2016/Timken_india.1.pdf',
        'reports/2016/Zandu_realty.1.pdf']

        for item in list:
            self.add_data_from_filename(item)


if __name__ == '__main__':
    langModel = LangModel()
    langModel.create_model_from_fixed_list()
    print(langModel.get_model_data())