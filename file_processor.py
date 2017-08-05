import os
from numpy import genfromtxt
from datetime import datetime
import os
import scipy
import math
import numpy

try:
    import Queue as Q  # ver. < 3.0
except ImportError:
    import queue as Q


percentang_change_column = 8

class holder:
    def __init__(self, data, name=''):
        self.id = ""
        self.name = name
        self.face_value = 0.0
        self.number_of_shares = 0.0
        self.data = data

def find_correlation(holder1, holder2):
    sec1 = []
    sec2 = []
    row1_count = 0
    row2_count = 0
    while(True):
        if len(holder1.data) - 1 <= row1_count or len(holder2.data) - 1 <= row2_count:
            break
        if (holder1.data[row1_count][0] > holder2.data[row2_count][0]):
            row1_count = row1_count + 1
        elif (holder1.data[row1_count][0] < holder2.data[row2_count][0]):
            row2_count = row2_count + 1
        else:
            break
    if holder1.data[row1_count][0] == holder2.data[row2_count][0]:

        #print holder1.data[row1_count][0] + ' = ' + holder2.data[row2_count][0]
    #else:
        while (holder1.data[row1_count][0] == holder2.data[row2_count][0]):
            sec1.append(float(holder1.data[row1_count][percentang_change_column]))
            sec2.append(float(holder2.data[row2_count][percentang_change_column]))
            row1_count = row1_count + 1
            row2_count = row2_count + 1
            if len(holder1.data) - 1 <= row1_count or len(holder2.data) - 1 <= row2_count:
                break

    #value = numpy.corrcoef(sec1, sec2)
    #print (value)
    return numpy.corrcoef(sec1, sec2)

def find_cross_correl(stocks):
    correlation = {}

    #find correlation between (price change | volume change | etc.) in %
    #this does not consider share splitting or change in base price
    for stock in stocks.keys():
        for inner_stock in stocks.keys():
            if stock == inner_stock:
                continue
            name = stock + '--' + inner_stock
            #find_correlation(stocks[stock], stocks[inner_stock])
            correl = find_correlation(stocks[stock], stocks[inner_stock])
            correlation[name] = correl
    return correlation

#dict that holds every security
stocks = {}

#read files. may be create a pickle later?
for file in os.listdir("data"):
    if file.endswith(".csv") and 'NSE' in file:
        file_path = os.path.join("data", file)
        f = open(file_path)
        data = genfromtxt(file_path, dtype=str, delimiter=",", skip_header=1)#,names=['x','y'])

        z = numpy.zeros((len(data),1))
        z[0] = 0.0
        first_row = data[0]
        first_row[0] = datetime.strptime(first_row[0], '%Y-%m-%d')
        for i in range(1, len(data)):
            row = data[i]
            prev_row = data[i - 1]
            row[0] = datetime.strptime(row[0], '%Y-%m-%d')
            try:
                z[i] = ((float(row[5]) - float(prev_row[5])) / float(prev_row[5]))
            except ValueError:
                z[i] = 0.0

        #add percentage change column to the data here
        data = numpy.append(data, z, axis=1)
        #print (data)
        stocks[file] = holder(data, name=file)
        #print (file_path)

correlation = find_cross_correl(stocks)

q = Q.PriorityQueue()

for key in correlation.keys():
    if len(correlation[key]) > 0 and not math.isnan(correlation[key][0][1]):
        q.put((correlation[key][0][1],key))
        '''if (correlation[key][0][1] > max):
            max = correlation[key][0][1]
            max_name = key
        '''
while not q.empty():
    print (q.get())
    q.get()
