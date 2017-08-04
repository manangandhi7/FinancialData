
from data_holder.Security import Security
import matplotlib

sec = Security()


"""
================
Date tick labels
================

Show how to make date plots in matplotlib using date tick locators and
formatters.  See major_minor_demo1.py for more information on
controlling major and minor ticks

All matplotlib date plotting is done by converting date instances into
days since the 0001-01-01 UTC.  The conversion, tick locating and
formatting is done behind the scenes so this is most transparent to
you.  The dates module provides several converter functions date2num
and num2date

"""
from datetime import datetime
import os
import matplotlib.dates as mdates
import numpy

#start

file_name='play_data\\TCS.csv'
file_name='data\\NSE-SCHNEIDER.csv'
date_format = '%d-%B-%Y'
date_format = '%Y-%m-%d' #NSE
closing_price_column = 5
ycolumn_to_plot = 7

datafile = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_name)

import matplotlib.pyplot as plt
from numpy import genfromtxt
data=genfromtxt(datafile, dtype=str, delimiter=",", skip_header=1)#,names=['x','y'])


daily_percentage_change = numpy.zeros((len(data),1))
daily_percentage_change[0] = 0.0
first_row = data[0]
for i in range(1, len(data)):
    row = data[i]
    prev_row = data[i - 1]
    try:
        daily_percentage_change[i] = ((float(prev_row[closing_price_column]) - float(row[closing_price_column])) / float(row[closing_price_column]))
        #print (str(row[5]) + '-' + str(prev_row[5]) + ' / '+ str(prev_row[5]) +' = ' + str(z[i]))
    except ValueError:
        daily_percentage_change[i] = 0.0

data = numpy.append(data, daily_percentage_change, axis=1)
x=[datetime.strptime(row[0], date_format) for row in data]
#y=[row[ycolumn_to_plot] for row in data]
y=[row[ycolumn_to_plot] for row in data]

'''
columnsize = int(len(x)/6)
ax=plt.subplot(111)
for i in range(columnsize):
    ax.plot(x,y)
plt.show()
'''
#end

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
yearsFmt = mdates.DateFormatter('%Y')

# open, close, volume, adj_close from the mpl-data/example directory.
# The record array stores python datetime.date as an object array in

fig, ax = plt.subplots()
ax.plot(x, y)

# format the ticks
ax.xaxis.set_major_locator(years)
ax.xaxis.set_major_formatter(yearsFmt)
ax.xaxis.set_minor_locator(months)

datemin = min(x)
datemax = max(x)
ax.set_xlim(datemin, datemax)

# format the coords message box
def price(x):
    return '$%1.2f' % x
ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
ax.format_ydata = price
ax.grid(True)

# rotates and right aligns the x labels, and moves the bottom of the
# axes up to make room for them
fig.autofmt_xdate()

plt.show()
