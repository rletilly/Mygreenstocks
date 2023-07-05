#Alpha vantage API key = W4ZX7JFKKRXMXROD can be use for their search endpoint utility 
#Financial modeling prep API Key : 963351a791575f888eed177dd9400e77 - 963351a791575f888eed177dd9400e77

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
#def get_historical_price():
#    stock_name = get_stock_name()
#    cls_prc = si.get_data(stock_name)
#    return cls_prc

#Plot the stock historic price by closing date 
#def plot_stock_price():
#    cls_prc = get_historical_price()
#    cls_prc = cls_prc.reset_index(names = "dates")
#    cls_prc.plot(x = 'dates', y = 'close')
#    plt.show()

#Transform dict to dataframe
def from_dict_to_dataframe(dictio, dictia):
    df = pd.DataFrame.from_dict(dictio)
    df1 = pd.DataFrame.from_dict(dictia)
    df2 = df[["date","companyName","ESGScore","environmentalScore", "socialScore", "governanceScore"]]
    df2.insert(6,"ESGRiskRating",df1[["ESGRiskRating"]])
    return df2

#On récupère les noms des clients
def get_stock_info():
    stock_name = []
    stock_amt = []
    answer = ""
    while (answer !="n"):
        stock_name.append(str(input("What is your stock name ? ")).upper())
        stock_amt.append(int(input("How many share have you ? ")))
        answer = str(input("You have another stock ? (y/n) "))
    return [stock_name, stock_amt]

#On trouve le poids de chaque titre
def get_weight():
    stock_info = get_stock_info()
    #On multiplie la quantité de stocks avec le prix T pour savoir qui pèse le plus lourd
    for i in range(0, len(stock_info[0])):
        stock_info[1][i]= stock_info[1][i]*get_stock_price(stock_info[0][i]) #[0][] = Nom / [1][] = Quantité
    return stock_info
    
#On plot le resultat dans un pie chart
def plot_stock_weight(): 
    stock = get_weight()
    fig, ax = plt.subplots()
    ax.pie(stock[0], labels=stock[1], autopct='%1.1f%%')
    plt.show()

    #On donne la valeur du ptf 
    print("Portfolio total value: "+ sum(stock[1]))

#Ici on fait la query au site et on transforme les deux dict en un dataframe 
def get_jsonparsed_data(name):
    url = ("https://financialmodelingprep.com/api/v4/esg-environmental-social-governance-data?symbol="+ name +"&apikey=963351a791575f888eed177dd9400e77")
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    df = json.loads(data)

    url2 = ("https://financialmodelingprep.com/api/v4/esg-environmental-social-governance-data-ratings?symbol="+ name +"&apikey=963351a791575f888eed177dd9400e77")
    response2 = urlopen(url2, cafile=certifi.where())
    data2 = response2.read().decode("utf-8")
    df2 = json.loads(data2)

    df_agg = from_dict_to_dataframe(df, df2)
    return df_agg

#Ici je créer une liste de dataframe 
def dataprep_dict():
    i = 0
    df=[]
    stock_info = get_stock_info() #[0][] = Nom / [1][] = Quantité
    while(i != len(stock_info[0])):
        df.append(get_jsonparsed_data(stock_info[0][i]))
        i+=1
    print(df)
     
    # Il faut encore que je multiplie les poids avec chaque valeurs
    # et je rends une unique avec en colonne chaque titre et en lignes chaque val 



#dataprep_dict()


#J'ai les prix et les profils il faut que je calcul les poids 
#Je traduis chaque note en chiffres 
note = [["CCC","CCC+","CC","CC+","C","C+","B","B+","BB","BB+","BBB","BBB+","A","A+","AA","AA+","AAA","AAA+"],
        [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18]]