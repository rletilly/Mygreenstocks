#Financial modeling prep API Key : 963351a791575f888eed177dd9400e77

import pandas as pd
import certifi
import json
from urllib.request import urlopen
from tkinter import messagebox
from tkinter import filedialog
import ssl

Api_Key = "963351a791575f888eed177dd9400e77"

#This is used for tkinter 
stock_list = [[],[]]

#This function is used anytime a call is made to the API
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
    ESG = [0,0,0,0]
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
        for j in range(0, 4):#note 
            ESG[j] += agg_score[i][str(df.columns[j])][0] * stock_info[1][i]* agg_price[i]["price"][0]
        divi += stock_info[1][i] * agg_price[i]["price"][0]

    messagebox.showinfo("Your results","La note "+ df.columns.values[0] +" moyenne la plus récente est de: " + str(round(ESG[0]/divi,2)) +
                        "\n\n"+"La note "+ df.columns.values[1] +" moyenne la plus récente est de: " + str(round(ESG[1]/divi, 2)) +
                        "\n\n"+"La note "+ df.columns.values[2] +" moyenne la plus récente est de: " + str(round(ESG[2]/divi,2)) +
                        "\n\n"+"La note "+ df.columns.values[3] +" moyenne la plus récente est de: " + str(round(ESG[3]/divi,2)))
    result_to_excel(agg_score,agg_grade)

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

#function that reads excel and fills "stock_list" with the ticker and the quantity, the list will be call when clicked on finished 
def browse_excel_file():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        df = pd.read_excel(file_path)
        read_excel(df) 

#Print your results to an excel
def result_to_excel(agg_score,agg_grade):
    headers = ["Stock","ESGRiskRating","environmentalScore", "socialScore","governanceScore","ESGScore"]
    val1 = []
    val2 = []
    for i in range(0,len(stock_list[0])):
        val1.append(agg_score[i].iloc[0].tolist())
        val2.append(agg_grade[i]["ESGRiskRating"][0])
    tval1 = list(map(list, zip(*val1)))
    
    rend = pd.DataFrame({headers[0]: stock_list[0], headers[1] : val2, headers[2] : tval1[0], headers[3] : tval1[1], headers[4] : tval1[2], headers[5] : tval1[3]})
    rend.to_excel('results.xlsx', index=False)
