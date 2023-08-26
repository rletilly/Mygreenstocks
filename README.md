# Mygreenstocks

This project is born so that people could easily have a picture of how sustainable their stock portfolio is.  

Please keep in min that I am using my personal API_KEY for now, we will be limited to **300 query a minute**. Else, you can easily change the API_KEY in the code, line 14.  

"best_in_class.xlsx" is an extract of the best stocks given by "Financial Data Prep". Keep in mind that this is regarding "ESG Risk Score" and not other grades.  

In case you wanted to download you stock portfolio directly, you can import it if it respects the format given in the file "your_stock_example.xlsx"  

The "gui.py" file has to be runned for the tool to launch.  

# Walkthrough

<h3>Step 1</h3>  
Here's what will be displayed at first :  
<p align="center"> 
<img src="https://github.com/rletilly/Mygreenstocks/assets/55627422/328efca4-bf0f-4d8b-9b7b-e0a02110b666" alt="drawing" width="200"/>
</p>

This is the window from where you will start your operations.  

- **"Stock Ticker"** is for stock symbols (NETFLIX -> NFLX)  
- **"Amount"** only accepts int numbers, for the number of stocks you have  
- **"Add Stock"** is to be pressed once you've succeddfully added a stock name and an amount  

- **"Import Excel"** will allow you to **import your portfolio** data in an excel file following the structure of "your_stock_example.xlsx" file  
- **"Help"** can be used if you do not know the ticker of your stock*  
- **"Finish"** **MUST be pressed** once you've finished using this window (even after loading an excel file)  
  
<h3>Step 2</h3> 
Once the "Finish" button is pressed, a charging indicator will show on the screen until the code has finished ( for the least patient of us ;D ).  

Two boxes are to be expected  

<p align="center"> 
<img src="https://github.com/rletilly/Mygreenstocks/assets/55627422/74bdaa8f-a26c-4245-83c2-607620f3b241" alt="drawing" width="400"/>
</p>

Your portfolio weighted ESG risk score. And  

<p align="center">
<img src="https://github.com/rletilly/Mygreenstocks/assets/55627422/95ae9957-30a0-46c9-aecb-0ba391c0e0f3" alt="drawing" width="400"/>
</p>

Your portfolio weighted ESG grades.  

<h3>Step 3</h3>  
Once you have clicked Ok on both windows the detailed results will be charged in the "results.xlsx" file.  

<br />
<br />
<br />
<h3>Help Button</h3>  
In the "Help" box :  
<p align="center">
<img src="https://github.com/rletilly/Mygreenstocks/assets/55627422/fda870a2-a681-41b8-b1c4-f62b3ae463a6" alt="drawing" width="400"/>
</p>

You can either enter **a ticker or a name**. It **doesn't have to be written entirely**, the query will search and display the closest ticker/name it has of your input.  

The number of response you get is fixed to 20 but it can be changed in the code (line 33 - MyGreenStocks.py).  

**Careful** This query is not bulletproof, I've found some results that were not working with other queries later one. Google will still be your best friend if you do not remember your ticker.  
