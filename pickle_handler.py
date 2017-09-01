__author__ = 'manan'

import pickle

def write_pickle(file_name, object):
    try:
        file = open(file_name, 'rb')
    except:
        with open(file_name, 'wb') as output:
            pickle.dump(object, output, pickle.HIGHEST_PROTOCOL)

def read_pickle(file_name):
    try:
        with open(file_name, 'rb') as input:
            pdf = pickle.load(input)
            return pdf
    except:
        return None
