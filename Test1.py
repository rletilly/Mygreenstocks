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
    for i in range(0, len(stock_amt)):
        stock_amt[i]= stock_amt[i]*get_stock_price(stock_name[i])
    
    #On plot le resultat dans un pie chart 
    fig, ax = plt.subplots()
    ax.pie(stock_amt, labels=stock_name, autopct='%1.1f%%')
    plt.show()

    #On donne la valeur du ptf 
    print("Portfolio total value: "+ sum(stock_amt))


def from_dict_to_dataframe(dictio, dictia):
    df = pd.DataFrame.from_dict(dictio)
    df1 = pd.DataFrame.from_dict(dictia)
    df2 = df[["date","companyName","ESGScore","environmentalScore", "socialScore", "governanceScore"]]
    df2[["ESGRiskRating"]] = df1[["ESGRiskRating"]]
    return df2

####################################################################### From dict to Dataframe ########################################################
dictio = [ {
    "symbol" : "AAPL",
    "cik" : "0000320193",
    "companyName" : "Apple Inc.",
    "formType" : "10-K",
    "acceptedDate" : "2021-10-28 18:04:28",
    "date" : "2021-09-25",
    "environmentalScore" : 26.22,
    "socialScore" : 20.36,
    "governanceScore" : 25.15,
    "ESGScore" : 23.91,
    "url" : "https://www.sec.gov/Archives/edgar/data/320193/000032019321000105/0000320193-21-000105-index.htm"
  }, {
    "symbol" : "AAPL",
    "cik" : "0000320193",
    "companyName" : "Apple Inc.",
    "formType" : "10-K",
    "acceptedDate" : "2020-10-29 18:06:25",
    "date" : "2020-09-26",
    "environmentalScore" : 21.61,
    "socialScore" : -1.12,
    "governanceScore" : 22.72,
    "ESGScore" : 14.4,
    "url" : "https://www.sec.gov/Archives/edgar/data/320193/000032019320000096/0000320193-20-000096-index.htm"
  }, {
    "symbol" : "AAPL",
    "cik" : "0000320193",
    "companyName" : "Apple Inc.",
    "formType" : "10-K",
    "acceptedDate" : "2020-10-29 18:06:25",
    "date" : "2019-09-26",
    "environmentalScore" : 21.61,
    "socialScore" : -1.12,
    "governanceScore" : 22.72,
    "ESGScore" : 14.4,
    "url" : "https://www.sec.gov/Archives/edgar/data/320193/000032019320000096/0000320193-20-000096-index.htm"
  }
]

dictia = [ {
    "symbol" : "AAPL",
    "cik" : "0000320193",
    "companyName" : "Apple Inc.",
    "industry" : "ELECTRONIC COMPUTERS",
    "year" : 2022,
    "ESGRiskRating" : "B+",
    "industryRank" : "3 out of 6"
  }, {
    "symbol" : "AAPL",
    "cik" : "0000320193",
    "companyName" : "Apple Inc.",
    "industry" : "ELECTRONIC COMPUTERS",
    "year" : 2021,
    "ESGRiskRating" : "B",
    "industryRank" : "6 out of 7"
  }
]

print(from_dict_to_dataframe(dictio, dictia))



