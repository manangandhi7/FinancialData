__author__ = 'manan'


import requests
import urllib


http_proxy  = "http://pxvip01.intranet.commerzbank.com:8080"
https_proxy  = "https://pxvip01.intranet.commerzbank.com:8080"

http_proxy  = "http://ZTB/cb2gano:hopa.1212@pxvip01.intranet.commerzbank.com:8080"
https_proxy  = "https://ZTB/cb2gano:hopa.1212@pxvip01.intranet.commerzbank.com:8080"

proxyDict = {
              "http"  : http_proxy,
              "https" : https_proxy,
            }

r = requests.get('http://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?scripcode=512289&flag=sp&Submit=G', proxies=proxyDict)
r.status_code
r = requests.get('http://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?scripcode=512289&flag=sp&Submit=G', proxies=urllib.getproxies())
r.status_code

#get data
#create correlations
#find the ones with highest correlation (positive and negative)
#also do the averaging
