#Alpha vantage API key = W4ZX7JFKKRXMXROD can be use for their search endpoint utility 
#Financial modeling prep API Key : 963351a791575f888eed177dd9400e77

import string
import pandas as pd
import requests
import alpha_vantage as av
import yahoo_fin.stock_info as si
from yahoo_fin import options
import certifi
import json
from urllib.request import urlopen
from fmp_python.fmp import FMP
import matplotlib.pyplot as plt

#get a live stock price from Yahoo
def get_stock_price(stck):
    return si.get_live_price(stck)

#Get a stock price and its historic from Yahoo
def get_historical_price():
    stock_name = get_stock_name()
    cls_prc = si.get_data(stock_name)
    return cls_prc

#Get a stock name from user
def get_stock_name():
    stock_name = str(input("What is your stock name ? "))
    return stock_name.upper()

#Plot the stock historic price by closing date 
def plot_stock_price():
    cls_prc = get_historical_price()
    cls_prc = cls_prc.reset_index(names = "dates")
    cls_prc.plot(x = 'dates', y = 'close')
    plt.show()


#Next steps are to get from user the number of shares and compute an average weight of the ptf with the price each year 

########################################################    MAIN   #################################################

####################################################################################################################








