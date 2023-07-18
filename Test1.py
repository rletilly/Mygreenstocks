#Alpha vantage API key = W4ZX7JFKKRXMXROD can be use for their search endpoint utility 
#Financial modeling prep API Key : 963351a791575f888eed177dd9400e77 - 963351a791575f888eed177dd9400e77


import pandas as pd
import alpha_vantage as av
import yahoo_fin.stock_info as si
from yahoo_fin import options
import certifi
import json
from urllib.request import urlopen
from fmp_python.fmp import FMP
import matplotlib.pyplot as plt
from openpyxl import load_workbook

#Je traduis chaque note en chiffres 
note = ["C","C+","CC","CC+","CCC","CCC+","B","B+","BB","BB+","BBB","BBB+","A","A+","AA","AA+","AAA"]

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


#J'ai les prix et les profils il faut que je calcul les poids 


def get_companies_names():
    print("You forgot the full name of your company or its ticker ? \nGive us some ideas, we'll search for you: ")
    name = input().upper()
    url = ("https://financialmodelingprep.com/api/v3/search?query="+name+"&limit=10&exchange=NYSE,NASDAQ,AMEX,TSX,ETF,EURONEXT,XETRA,ASX,SIX,HKSE,NSE&apikey=963351a791575f888eed177dd9400e77")
    #Exchanges for now : NYSE,NASDAQ,AMEX,TSX,ETF,EURONEXT,XETRA,ASX,SIX,HKSE,NSE
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    liste = json.loads(data)
    df = pd.DataFrame(liste)
    print(df[["symbol", "name"]])


def ESG_Score(note):
    agg_score = []
    agg_grade = []
    agg_price = []
    somme = 0
    divider = 0
    stock_info = [["NFLX","AAPL", "LVMHF"],[4,5,1]]#get_stock_info()
    for i in range(0, len(stock_info[0])):
        ################################## get ESG score #################################
        url = ("https://financialmodelingprep.com/api/v4/esg-environmental-social-governance-data?symbol="+stock_info[0][i]+"&apikey=963351a791575f888eed177dd9400e77")
        response = urlopen(url, cafile=certifi.where())
        data = response.read().decode("utf-8")
        liste = json.loads(data)
        df = pd.DataFrame(liste)
        df = df.drop(columns=["symbol","cik","companyName","formType","acceptedDate","url"], axis=1)
        ##################################################################################
        ################################## get ESG grade #################################
        url = ("https://financialmodelingprep.com/api/v4/esg-environmental-social-governance-data-ratings?symbol="+stock_info[0][i]+"&apikey=963351a791575f888eed177dd9400e77")
        response = urlopen(url, cafile=certifi.where())
        data = response.read().decode("utf-8")
        liste = json.loads(data)
        df2 = pd.DataFrame(liste)
        df2 = df2.drop(columns=["symbol","cik","companyName","industry","industryRank"], axis=1)
        ##################################################################################
        ################################# get Stock Price ################################
        url = ("https://financialmodelingprep.com/api/v3/quote-short/"+stock_info[0][i]+"?apikey=963351a791575f888eed177dd9400e77")
        response = urlopen(url, cafile=certifi.where())
        data = response.read().decode("utf-8")
        liste = json.loads(data)
        df3 = pd.DataFrame(liste)
        df3 = df3.drop(columns=["symbol", "volume"], axis=1)
        #################################################################################
        agg_score.append(df)
        agg_grade.append(df2)
        agg_price.append(df3)
    #################################### get Average grade ##############################    
    for i in range(0, len(stock_info[0])):
        somme += (note.index(agg_grade[i]["ESGRiskRating"][0])+1) * stock_info[1][i] * agg_price[i]["price"][0]
        divider += stock_info[1][i]* agg_price[i]["price"][0]
    print("La note globale, moyenne, pondérée la plus récente ("+str(agg_grade[0]["year"][0])+") est de: " + note[round(somme/divider)])


ESG_Score(note)




















#Alpha vantage API key = W4ZX7JFKKRXMXROD can be use for their search endpoint utility 
#Financial modeling prep API Key : 963351a791575f888eed177dd9400e77 - 963351a791575f888eed177dd9400e77

import pandas as pd
import certifi
import json
from urllib.request import urlopen
#from fmp_python.fmp import FMP #A voir si on dégage
import matplotlib.pyplot as plt

#TO DO : 
#Brancher la fonction ESG au bouton
# Do the same but with other metrics
#Do it for each year (can be done later on)
#Demander quand vont arriver les données de 2023

#This array is every possible ESG risk score possible with my tool 
note = ["C","C+","CC","CC+","CCC","CCC+","B","B+","BB","BB+","BBB","BBB+","A","A+","AA","AA+","AAA"]

#This is used for tkinter 
stock_list = []

#This fucntion is used anytime a call is made to the APi ---- Il faut mettre un try la dessus et retourner une phrase si pas de réponse de la part de l'API - Seuelemtn si on pred une erreur lors d'une fausse query
def API_call(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    liste = json.loads(data)
    df = pd.DataFrame(liste)
    return df

#Transform dict to dataframe
def from_dict_to_dataframe(dictio, dictia):
    df = pd.DataFrame.from_dict(dictio)
    df1 = pd.DataFrame.from_dict(dictia)
    df2 = df[["date","companyName","ESGScore","environmentalScore", "socialScore", "governanceScore"]]
    df2.insert(6,"ESGRiskRating",df1[["ESGRiskRating"]])
    return df2

#Get stock name and amount --> To be transformed with a python box and merged with get_companies_names
def get_stock_info():
    stock_name = []
    stock_amt = []
    answer = ""
    while (answer !="n"):
        stock_name.append(str(input("What is your stock name ? ")).upper())
        stock_amt.append(int(input("How many share have you ? ")))
        answer = str(input("You have another stock ? (y/n) "))
    return [stock_name, stock_amt]

#This function aim to help the user find its stock ticker our name
#Exchanges for now : NYSE,NASDAQ,AMEX,TSX,ETF,EURONEXT,XETRA,ASX,SIX,HKSE,NSE --------- A voir avec MUTUAL_FUND, INDEX, LSE
def get_companies_names(name):
    url = ("https://financialmodelingprep.com/api/v3/search?query="+name+"&limit=20&exchange=NYSE,NASDAQ,AMEX,TSX,ETF,EURONEXT,XETRA,ASX,SIX,HKSE,NSE&apikey=963351a791575f888eed177dd9400e77")
    df = API_call(url)
    df = df.drop(columns=["currency", "stockExchange"], axis=1)
    return df

#This function returns the last average risk score of a portfolio --> Can be done with the other metrics - to be plugged and modify with API and button 
def ESG_Score(note):
    agg_score = []
    agg_grade = []
    agg_price = []
    ESG = [0,0,0]
    divi = [,0,0,0]
    somme = 0
    divider = 0
    stock_info = [["NFLX","AAPL", "LVMHF"],[4,5,1]]#get_stock_info()
    for i in range(0, len(stock_info[0])):
        ################################## get ESG score #################################
        url = ("https://financialmodelingprep.com/api/v4/esg-environmental-social-governance-data?symbol="+stock_info[0][i]+"&apikey=963351a791575f888eed177dd9400e77")
        df = API_call(url)
        df = df.drop(columns=["symbol","cik","companyName","formType","acceptedDate","url"], axis=1)
        ##################################################################################
        ################################## get ESG grade #################################
        url = ("https://financialmodelingprep.com/api/v4/esg-environmental-social-governance-data-ratings?symbol="+stock_info[0][i]+"&apikey=963351a791575f888eed177dd9400e77")
        df2 = API_call(url)
        df2 = df2.drop(columns=["symbol","cik","companyName","industry","industryRank"], axis=1)
        ##################################################################################
        ################################# get Stock Price ################################
        url = ("https://financialmodelingprep.com/api/v3/quote-short/"+stock_info[0][i]+"?apikey=963351a791575f888eed177dd9400e77")
        df3 = API_call(url)
        df3 = df3.drop(columns=["symbol", "volume"], axis=1)
        #################################################################################
        agg_score.append(df)
        agg_grade.append(df2)
        agg_price.append(df3)
    #################################### get Average grade ##############################    
    for i in range(0, len(stock_info[0])):
        somme += (note.index(agg_grade[i]["ESGRiskRating"][0])+1) * stock_info[1][i] * agg_price[i]["price"][0]
        divider += stock_info[1][i]* agg_price[i]["price"][0]
    print("La note globale, moyenne, pondérée la plus récente ("+str(agg_grade[0]["year"][0])+") est de: " + note[round(somme/divider)-1])

    ################################### get Average score ###############################
    for i in range(0, len(stock_info)):
        for j in range (0,3):
            ESG[i] += agg_score[j][stock_info[0][j]][0] * stock_info[1][j] * agg_price[j]["price"][0]
            divi[i] += stock_info[1][j] * agg_price[j]["price"][0]
    for i in range(0, len(divi)):
        ESG[i] = ESG[i]/divi[i]
        print("La note "+ df.columns.values[i] +" moyenne, pondérée la plus récente ("+str(agg_grade[0]["year"][0])+") est de: " + ESG[i]) 


################################################################################################################ PAS UTILISÉS #######################################################################################
#On trouve le poids de chaque titre --> Avoir si on garde cette fonction, utilisée par plot stock weight 
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

#####################################################################################################################################################################################################################
######################################################################### GUI - GRAPHICAL USER INTERFACE ############################################################################################################
#####################################################################################################################################################################################################################

import tkinter as tk
from tkinter import messagebox
from tkinter import *

#Function that takes user input and display them at the end - Must return the stock list once it's over 
def add_stock():
    stock_name = stock_entry.get()
    stock_amount = amount_entry.get()
    if stock_name and stock_amount:
        stock_list.append((stock_name.upper(), stock_amount))
        stock_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter stock name and amount.")

#Function that call the search function if user forgot it's company tiker -------------------------- NEED TO BE TESTED WITH API CALL - Does it work with non MAJ ??
def search_stock():
    stock_name = stock_entry2.get()
    poss_windo = Tk()
   
    if stock_name :
        poss_windo.title("Possible ticker and stocks")
        poss_windo.geometry("300x400")
        df = get_companies_names(stock_name)
        
        # insert dataframe into the possible stock window
        n_rows = df.shape[0]
        n_cols = df.shape[1]
        column_names = df.columns
        i=0
        for j, col in enumerate(column_names):
            text = Text(poss_windo, width=16, height=1, bg = "#9BC2E6")
            text.grid(row=i,column=j)
            text.insert(INSERT, col)

        for i in range(n_rows):
            for j in range(n_cols):
                text = Text(poss_windo, width=16, height=1)
                text.grid(row=i+1,column=j)
                text.insert(INSERT, df.loc[i][j])

        stock_entry2.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter stock name.")

    poss_windo.mainloop()

#Function to delete the window once it's done 
def finish_input(window):
    if len(stock_list) >= 0:
        for stock in stock_list:
            print(f"Stock Name: {stock[0]}, Amount: {stock[1]}")
        window.destroy()
    else:
        messagebox.showwarning("Input Error", "Please enter at least one stock.")

#Function to take stocks as input 
def add_stock_window():
    global stock_entry, amount_entry

    stock_window = Tk()
    stock_window.title("Stock Input")

    stock_label = tk.Label(stock_window, text="Stock Ticker:")
    stock_label.grid(row=0, column=0, padx=10, pady=10)

    stock_entry = tk.Entry(stock_window)
    stock_entry.grid(row=0, column=1, padx=10, pady=10)

    amount_label = tk.Label(stock_window, text="Amount:")
    amount_label.grid(row=1, column=0, padx=10, pady=10)

    amount_entry = tk.Entry(stock_window)
    amount_entry.grid(row=1, column=1, padx=10, pady=10)

    add_button = tk.Button(stock_window, text="Add Stock", command=add_stock)
    add_button.grid(row=2, column=0, padx=10, pady=10)

    finish_button = tk.Button(stock_window, text="Finish", command=lambda: finish_input(stock_window))
    finish_button.grid(row=2, column=1, columnspan=1, padx=10, pady=10)

    help_button = tk.Button(stock_window, text="help", command=add_help_window)
    help_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    
    stock_window.mainloop()
    
#Function to have help as a window 
def add_help_window():
    global stock_entry2

    help_window = Tk()
    help_window.title("Help")

    stock_label = tk.Label(help_window, text="Stock Name or Ticker:")
    stock_label.grid(row=0, column=0, padx=10, pady=10)

    stock_entry2 = tk.Entry(help_window)
    stock_entry2.grid(row=0, column=1, padx=10, pady=10)

    add_button = tk.Button(help_window, text="Search", command=search_stock)
    add_button.grid(row=2, column=0, padx=10, pady=10)

    finish_button = tk.Button(help_window, text="Finish", command= lambda: finish_input(help_window))
    finish_button.grid(row=2, column=1, columnspan=1, padx=10, pady=10)
    
    help_window.mainloop()

#add_stock_window()



################################################################## WHO ARE THE BEST IN CLASS ?? ###############################################################################

import time
# Voir le nombre de ticker sur la premiere query et le nombre sur la deuxième 
#url = ("https://financialmodelingprep.com/api/v3/stock/list?apikey=YOUR_API_KEY") --> Nous donne la possibilité de voir tous les traded and non traded stocks - 25k

def best_in_class(): 
    url = ("https://financialmodelingprep.com/api/v3/stock/list?apikey=YOUR_API_KEY")
    df = API_call(url)
    df = df.drop(columns=["price","exchange"], axis=1)
    #we write in the excel
    df.to_excel(excel_writer="Path")
    for i in range (0,10):
        url = ("https://financialmodelingprep.com/api/v4/esg-environmental-social-governance-data-ratings?symbol="+ df["symbol"][i] +"&apikey=963351a791575f888eed177dd9400e77")
        df2 = API_call(url)
        df2 = df2.drop(columns=["symbol","cik","companyName","industry","industryRank"], axis=1)
        if i % 300 == 0:
            time.sleep(60)
        if df2["year"][0] == "2022":
            df2["ESGRiskRating"][0].to_excel(excel_writer="Path", startcol = 3)
        else:
            continue
        

 
