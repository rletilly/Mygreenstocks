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

def get_stock_amount():
    stock_amt = int(input("How many share have you ? "))
    return stock_amt

#Plot the stock historic price by closing date 
def plot_stock_price():
    cls_prc = get_historical_price()
    cls_prc = cls_prc.reset_index(names = "dates")
    cls_prc.plot(x = 'dates', y = 'close')
    plt.show()


#Next steps are to get from user the number of shares and compute an average weight of the ptf with the price each year 

########################################################    MAIN   #################################################

####################################################################################################################

#Plot the weight per stock in a pie chart 
def plot_stock_weight():
    stock_name = []
    stock_amt = []
    answer = ""

    #On récupère les noms et quantité de stock de la personne 
    while (answer !="n"):
        stock_name.append(get_stock_name())
        stock_amt.append(get_stock_amount())
        answer = str(input("You have another stock ? (y/n) "))

    #On multiplie la quantité de stocks avec le prix T pour savoir qui pèse le plus lourd
    #for i in range(0, len(stock_amt)):
    #    stock_amt[i]= stock_amt[i]*get_stock_price(stock_name[i])
    
    #On plot le resultat dans un pie chart 
    fig, ax = plt.subplots()
    ax.pie(stock_amt, labels=stock_name, autopct='%1.1f%%')
    plt.show()

    #On donne la valeur du ptf 
    print("Portfolio total value: "+ sum(stock_amt))






