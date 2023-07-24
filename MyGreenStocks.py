#Alpha vantage API key = W4ZX7JFKKRXMXROD can be use for their search endpoint utility 
#Financial modeling prep API Key : 963351a791575f888eed177dd9400e77 - 963351a791575f888eed177dd9400e77

import pandas as pd
import certifi
import json
from urllib.request import urlopen
import matplotlib.pyplot as plt

#TO DO : 
#Import excel file
#Demander quand vont arriver les données de 2023

#This is used for tkinter 
stock_list = [[],[]]

#This fucntion is used anytime a call is made to the APi
def API_call(url):
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    if data != "[]":
        liste = json.loads(data)
        df = pd.DataFrame(liste)
        return df
    else:
        messagebox.showwarning("Wrong API call","No return from the API with this URL:\n " + url + "\n\nMaybe check stock ticker or API key")

#This function aim to help the user find its stock ticker our name
#Exchanges for now : NYSE,NASDAQ,AMEX,TSX,ETF,EURONEXT,XETRA,ASX,SIX,HKSE,NSE,LSE,INDEX
def get_companies_names(name):
    url = ("https://financialmodelingprep.com/api/v3/search?query="+name+"&limit=20&exchange=NYSE,NASDAQ,AMEX,TSX,ETF,EURONEXT,XETRA,ASX,SIX,HKSE,NSE,LSE,INDEX&apikey=963351a791575f888eed177dd9400e77")
    df = API_call(url)
    df = df.drop(columns=["currency", "stockExchange"], axis=1)
    return df

#This function returns the last average risk score, and ESG grade of a Ptf --> When finished, add try/except
def ESG_Score(stock_info):
    note = ["C","C+","CC","CC+","CCC","CCC+","B","B+","BB","BB+","BBB","BBB+","A","A+","AA","AA+","AAA"]# All possible grade
    agg_score = []
    agg_grade = []
    agg_price = []
    ESG = [0,0,0]
    somme = 0
    divi = 0
    divider = 0
    
    for i in range(0, len(stock_info[0])):
        ################################## get ESG score #################################
        url = ("https://financialmodelingprep.com/api/v4/esg-environmental-social-governance-data?symbol="+stock_info[0][i]+"&apikey=963351a791575f888eed177dd9400e77")
        df = API_call(url)
        df = df.drop(columns=["symbol","cik","companyName","formType","acceptedDate","date","url"], axis=1)
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
#A mettre dans une boxe en non pas dans le terminal --> A sortir des boucles for 
    print("La note globale, moyenne, pondérée la plus récente ("+str(agg_grade[0]["year"][0])+") est de: " + note[round(somme/divider)-1])
    ################################### get Average score ###############################
    for i in range(0, len(stock_info[0])):
        for j in range (0,len(stock_info[0])):
            ESG[i] += agg_score[j][str(df.columns[i])][0] * stock_info[1][j] * agg_price[j]["price"][0]
        divi += stock_info[1][i] * agg_price[i]["price"][0]
    for i in range(0, len(ESG)):
        ESG[i] = ESG[i]/divi
#A mettre dans une boxe en non pas dans le terminal --> A sortir des boucles for 
        print("La note "+ df.columns.values[i] +" moyenne, pondérée la plus récente ("+ str(agg_grade[0]["year"][0])+") est de: " + str(ESG[i])) 

#####################################################################################################################################################################################################################
######################################################################### GUI - GRAPHICAL USER INTERFACE ############################################################################################################
#####################################################################################################################################################################################################################
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import *

#Function that takes user input and stores it in a global variable  
def add_stock():
    stock_name = stock_entry.get()
    stock_amount = amount_entry.get()
    try:
        if stock_name and stock_amount:
            stock_list[0].append(stock_name.upper())
            stock_list[1].append(int(stock_amount))
            stock_entry.delete(0, tk.END)
            amount_entry.delete(0, tk.END)
    except:
        messagebox.showwarning("Input Error", "Please enter stock name and amount.")
        stock_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)

#Function that call the search function if user forgot it's company ticker
def search_stock():
    stock_name = stock_entry2.get()
    poss_windo = Tk()
   
    if stock_name :
        poss_windo.title("Possible ticker and stocks")
        poss_windo.geometry("450x400")
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
                text = Text(poss_windo, width=20, height=1)
                text.grid(row=i+1,column=j)
                text.insert(INSERT, df.loc[i][j])

        stock_entry2.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please enter stock name.")

    poss_windo.mainloop()

#Function to delete the window once it's done 
def finish_input(window):
    if stock_list:
        window.destroy()
        ESG_Score(stock_list)
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
    help_button.grid(row=3, column=1, columnspan=3, padx=10, pady=10)

    import_button = tk.Button(stock_window, text="Import Excel", command=browse_excel_file)
    import_button.grid(row=3, column=0, columnspan=1,padx=10, pady=10)
    
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

def browse_excel_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        df = pd.read_excel(file_path)
#function that reads excel and fills "stock_list" with the ticker and the quantity, the list will be call when clicked on finished 

add_stock_window()

###############################################################################################################################################################################################################
################################################################################## BEST IN CLASS - Run Once a Year ############################################################################################
###############################################################################################################################################################################################################
from openpyxl import load_workbook

#Function that first write all tickers available in an excel and then check for each ticker it's ESG Risk Score
#This is a workaround to a query it don't have access to yet - Takes a few hours to complete - 40K records
def best_in_class(): 
    url = ("https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey=963351a791575f888eed177dd9400e77")
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    liste = json.loads(data)
    df = pd.DataFrame(liste)
    df.columns = ["symbol"]
    df.to_excel('best_in_class.xlsx', index=False)
    wb = load_workbook('best_in_class.xlsx')
    sheet = wb.active
    for i in range (1,len(df)): 
        url = ("https://financialmodelingprep.com/api/v4/esg-environmental-social-governance-data-ratings?symbol="+df["symbol"][i-1]+"&apikey=963351a791575f888eed177dd9400e77")
        response = urlopen(url, cafile=certifi.where())
        data = response.read().decode("utf-8")    
        if data !="[]":
            liste = json.loads(data)
            df2 = pd.DataFrame(liste)
            df2 = df2.drop(columns=["symbol","cik","industry","industryRank"], axis=1)
            sheet['B'+str(i+1)] = df2["ESGRiskRating"][0]
            sheet['C'+str(i+1)] = df2["companyName"][0]
            
    wb.save('best_in_class.xlsx')

#best_in_class()
################################################################################################################################################################################################################
