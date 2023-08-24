#Financial modeling prep API Key : 963351a791575f888eed177dd9400e77

import pandas as pd
import certifi
import json
from urllib.request import urlopen
import matplotlib.pyplot as plt
import ssl

Api_Key = "963351a791575f888eed177dd9400e77"

#This is used for tkinter 
stock_list = [[],[]]

#This fucntion is used anytime a call is made to the API
def API_call(url):
    context = ssl.create_default_context(cafile=certifi.where())
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    if data != "[]":
        liste = json.loads(data)
        df = pd.DataFrame(liste)
        return df
    else:
        messagebox.showwarning("Erreur appel de l'API","Pas de retour de la part de l'API avec cet URL:\n " + url + "\n\nCorrigez le ticker ou la clé API" 
        + "\nUne erreur d'appel peut aussi vouloir dire qu'il n'existe pas de données sur le ticker fourni")

#This function aim to help the user find its stock ticker or name
#Exchanges for now : NYSE,NASDAQ,AMEX,TSX,ETF,EURONEXT,XETRA,ASX,SIX,HKSE,NSE,LSE,INDEX
def get_companies_names(name):
    url = ("https://financialmodelingprep.com/api/v3/search?query="+name+"&limit=20&exchange=NYSE,NASDAQ,AMEX,TSX,ETF,EURONEXT,XETRA,ASX,SIX,HKSE,NSE,LSE,INDEX&apikey="+Api_Key)
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
        url = ("https://financialmodelingprep.com/api/v4/esg-environmental-social-governance-data?symbol="+stock_info[0][i]+"&apikey="+Api_Key)
        df = API_call(url)
        df = df.drop(columns=["symbol","cik","companyName","formType","acceptedDate","date","url"], axis=1)
        ##################################################################################
        ################################## get ESG grade #################################
        url = ("https://financialmodelingprep.com/api/v4/esg-environmental-social-governance-data-ratings?symbol="+stock_info[0][i]+"&apikey="+Api_Key)
        df2 = API_call(url)
        df2 = df2.drop(columns=["symbol","cik","companyName","industry","industryRank"], axis=1)
        ##################################################################################
        ################################# get Stock Price ################################
        url = ("https://financialmodelingprep.com/api/v3/quote-short/"+stock_info[0][i]+"?apikey="+Api_Key)
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
    messagebox.showinfo("Your results","La note globale, moyenne la plus récente est de: " + note[round(somme/divider)-1])
    ################################### get Average score ###############################
    for i in range(0, len(stock_info[0])): 
        for j in range(0, 3):#note 
            ESG[j] += agg_score[i][str(df.columns[j])][0] * stock_info[1][i]* agg_price[i]["price"][0]
        divi += stock_info[1][i] * agg_price[i]["price"][0]

    messagebox.showinfo("Your results","La note "+ df.columns.values[0] +" moyenne la plus récente est de: " + str(round(ESG[0]/divi,2)) +
                        "\n\n"+"La note "+ df.columns.values[1] +" moyenne la plus récente est de: " + str(round(ESG[1]/divi, 2)) +
                        "\n\n"+"La note "+ df.columns.values[2] +" moyenne la plus récente est de: " + str(round(ESG[2]/divi,2))) 
    result_to_excel(df,df2,stock_info)


def result_to_excel(df, df2, stock_info):
    #write results in an excel -> name/sheet name could be given by user 

    
#Reads an excel file given by user that respects the topology
def read_excel(df):
    for i in range (0, len(df)):
        if df["ticker"][i]:
            stock_list[0].append(df["ticker"][i].upper())
        else:
            tik = get_companies_names(df["name"][i])
            stock_list[0].append(tik["Companyname"][0])

        if df["amount"][i] != 0 and not isinstance(df["amount"][i], str):
            stock_list[1].append(df["amount"][i])
        else:
            messagebox.showwarning("Lecture fichier excel", "Nous n'acceptons que des quantités mumérique, Vérifiez votre fichier")
            quit()
 
    return stock_list

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
        messagebox.showwarning("Erreur Input", "Veuillez entrer un ticker et une quantité.")
        stock_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)

#Function that call the search function if user forgot it's company ticker
def search_stock():
    stock_name = stock_entry2.get()
    poss_windo = Tk()
   
    if stock_name :
        poss_windo.title("Ticker et Stocks possibles")
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
        messagebox.showwarning("Erreur Input", "Veuillez entrer un nom de stock")

    poss_windo.mainloop()

#Function to delete the window once it's done 
def finish_input(window):
    if stock_list:
        window.destroy()
        ESG_Score(stock_list)
    else:
        messagebox.showwarning("Erreur Input", "Veuillez entrer au moins 1 stock.")
        
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

#function that reads excel and fills "stock_list" with the ticker and the quantity, the list will be call when clicked on finished 
def browse_excel_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        df = pd.read_excel(file_path)
        read_excel(df)

add_stock_window()

###############################################################################################################################################################################################################
################################################################################## BEST IN CLASS - Run Once a Year ############################################################################################
###############################################################################################################################################################################################################
from openpyxl import load_workbook

#Function that first write all tickers available in an excel and then check for each ticker it's ESG Risk Score
#This is a workaround to a query it don't have access to yet - Takes a few hours to complete - 40K records
def best_in_class(): 
    url = ("https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey="+Api_Key)
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    liste = json.loads(data)
    df = pd.DataFrame(liste)
    df.columns = ["symbol"]
    df.to_excel('best_in_class.xlsx', index=False)
    wb = load_workbook('best_in_class.xlsx')
    sheet = wb.active
    for i in range (1,len(df)): 
        url = ("https://financialmodelingprep.com/api/v4/esg-environmental-social-governance-data-ratings?symbol="+df["symbol"][i-1]+"&apikey="+Api_Key)
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
