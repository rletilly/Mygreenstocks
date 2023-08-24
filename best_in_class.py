###############################################################################################################################################################################################################
################################################################################## BEST IN CLASS - Run Once a Year ############################################################################################
###############################################################################################################################################################################################################
from openpyxl import load_workbook
import pandas as pd
import certifi
import json
from urllib.request import urlopen
import ssl

Api_Key = "963351a791575f888eed177dd9400e77"

#Function that first write all tickers available in an excel and then check for each ticker it's ESG Risk Score
#This is a workaround to a query it don't have access to yet - Takes a few hours to complete - 40K records
def best_in_class(): 
    url = ("https://financialmodelingprep.com/api/v3/financial-statement-symbol-lists?apikey="+Api_Key)
    context = ssl.create_default_context(cafile=certifi.where())
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    liste = json.loads(data)
    df = pd.DataFrame(liste)
    df.columns = ["symbol"]
    df.to_excel('best_in_class.xlsx', index=False)
    wb = load_workbook('best_in_class.xlsx')
    sheet = wb.active
    for i in range (1,len(df)): 
        url = ("https://financialmodelingprep.com/api/v4/esg-environmental-social-governance-data-ratings?symbol="+df["symbol"][i-1]+"&apikey="+Api_Key)
        context = ssl.create_default_context(cafile=certifi.where())
        response = urlopen(url, context=context)
        data = response.read().decode("utf-8")    
        if data !="[]":
            liste = json.loads(data)
            df2 = pd.DataFrame(liste)
            df2 = df2.drop(columns=["symbol","cik","industry","industryRank"], axis=1)
            sheet['B'+str(i+1)] = df2["ESGRiskRating"][0]
            sheet['C'+str(i+1)] = df2["companyName"][0]
            
    wb.save('best_in_class.xlsx')

best_in_class()
