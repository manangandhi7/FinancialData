import os
from numpy import genfromtxt
from datetime import datetime
import os
import matplotlib.dates as mdates
import scipy
import math
import numpy


percentang_change_column = 6

class holder:
    def __init__(self, data, name=''):
        self.id = ""
        self.name = name
        self.face_value = 0.0
        self.number_of_shares = 0.0
        self.data = data
        print 'new sec initialized!'

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
            sec1.append(holder1.data[row1_count][percentang_change_column])
            sec2.append(holder2.data[row2_count][percentang_change_column])
            row1_count = row1_count + 1
            row2_count = row2_count + 1
            if len(holder1.data) - 1 <= row1_count or len(holder2.data) - 1 <= row2_count:
                break

    #value = numpy.corrcoef(sec1, sec2)
    #print (value)
    return numpy.corrcoef(sec1, sec2)


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
                #print (str(row[5]) + '-' + str(prev_row[5]) + ' / '+ str(prev_row[5]) +' = ' + str(z[i]))
            except ValueError:
                z[i] = 0.0

        #add percentage change column to the data here
        data = numpy.append(data, z, axis=1)
        #print (data)
        stocks[file] = holder(data, name=file)
        #print (file_path)

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

max = -2.0
max_name = ''
min = 2.0
min_name = ''

for key in correlation.keys():
    if len(correlation[key]) > 0 and not math.isnan(correlation[key][0][1]):
        if (correlation[key][0][1] > max):
            max = correlation[key][0][1]
            max_name = key
        if (correlation[key][0][1] < min):
            min = correlation[key][0][1]
            min_name = key

print ('\nmax_name = ' + max_name)
print ('max = ' + str(max))
print ('\nmin_name = ' + min_name)
print ('min = ' + str(min))
