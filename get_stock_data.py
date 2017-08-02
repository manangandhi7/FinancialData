import requests
import urllib

#TODO : add cookie
r = requests.get('http://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?scripcode=512289&flag=sp&Submit=G')
r.status_code
