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



################################## extract excel - one time only ######################################
import openpyxl

symbol = [ 
  "02M.DE", "0A00.L", "0A02.L", "0A05.L", "0A0C.L", "0A0D.L", "0A0E.L", "0A0F.L", "0A0H.L", "0A0I.L", "0A0J.L", 
  "0A0K.L", "0A0L.L", "0A0M.L", "0A0S.L", "0A0V.L", "0A0W.L", "0A0X.L", "0A10.L", "0A14.L", "0A15.L", "0A18.L", "0A1C.L", 
  "0A1J.L", "0A1K.L", "0A1L.L", "0A1M.L", "0A1N.L", "0A1O.L", "0A1R.L", "0A1S.L", "0A1U.L", "0A1V.L", "0A1W.L", "0A1X.L",
  "0A20.L", "0A21.L", "0A23.L", "0A26.L", "0A27.L", "0A28.L", "0A29.L", "0A2A.L", "0A2G.L", "0A2H.L", "0A2I.L", "0A2O.L", 
  "0A2P.L", "0A2S.L", "0A2T.L", "0A2X.L", "0A2Z.L", "0A33.L", "0A34.L", "0A36.L", "0A37.L", "0A39.L", "0ACT.L", "0AH3.L",
  "0AH7.L", "0AHI.L", "0AHJ.L", "0AI4.L", "0AJ1.L", "0AR9.L", "0B67.L", "0BDR.L", "0BFA.L", "0BJP.L", "0BNT.L", "0C6Y.L", 
  "0CDX.L", "0CHZ.L", "0CIJ.L", "0CUM.L", "0CUN.L", "0CXC.L", "0D00.L", "0D1X.L", "0DDP.L", "0DH7.L", "0DHC.L", "0DHJ.L", 
  "0DI7.L", "0DJI.L", "0DJV.L", "0DK7.L","0DK9.L", "0DKX.L", "0DLI.L", "0DMQ.L", "0DNH.L", "0DNW.L", "0DO7.L", "0DOL.L", 
  "0DOS.L", "0DP0.L", "0DP4.L", "0DPB.L", "0DPM.L", "0DPU.L", "0DQ7.L", "0DQK.L", "0DQZ.L", "0DRH.L", "0DRV.L", "0DSJ.L", 
  "0DTF.L", "0DTI.L", "0DTK.L", "0DU3.L", "0DUI.L", "0DUK.L", "0DVE.L", "0DVR.L", "0DWL.L", "0DWV.L", "0DXG.L", "0DXU.L", 
  "0DYD.L", "0DYQ.L", "0DZ0.L", "0DZC.L", "0DZJ.L", "0E1L.L", "0E1Y.L", "0E3C.L", "0E4K.L", "0E4Q.L", "0E5M.L", "0E6Y.L", 
  "0E7S.L", "0E7Z.L", "0E9V.L", "0EA2.L", "0EAQ.L", "0EAW.L", "0EBQ.L", "0EDD.L", "0EDE.L"
]

a = 105/100
print(a)



def get_companies_names():
  url = ("https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey=963351a791575f888eed177dd9400e77")
  response = urlopen(url, cafile=certifi.where())
  data = response.read().decode("utf-8")
  list_symbol = json.loads(data)
  iter = len(list_symbol)+51
  for i in range (0,10): #tester d'abord
    #Ici j'appelle l'API, dans l'idéal je sors le nom de la companie et j'ajoute le nom à la feuille excel dans la colonne 2


  df_symbol = pd.DataFrame(list_symbol, columns=["Symbol"])

  df_symbol.to_excel('output.xls', engine='openpyxl')

  #security name / Company name = ESG score query 
  # startrow int, default 0 Upper left cell row to dump data frame.
  # startcol int, default 0 Upper left cell column to dump data frame.

  #En js on demande le nom complet et ont fait le switch dans le df derriere
