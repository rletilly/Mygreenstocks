# Mygreenstocks

This project is born so that people could easily have a picture of how sustainable their stock portfolio is.

Please keep in min that I am using my personal API_KEY for now, we will be limited to 300 query a minute (if still up). Else, you can easily change the API_KEY in the code, line 14. 

You will find a Python file to run on your machine or a .exe button in the dist file.

"best_in_class.xlsx" is an extract of the best stocks given by "Financial Data Prep". Keep in mind that this is regarding "ESG Risk Score" and not other grades.

In case you wanted to download you stock portfolio directly, you can import it if it respects the format given in the file "your_stock_example.xlsx"


# Walkthrough

Here's what you can expect while using this tool : 

![image](https://github.com/rletilly/Mygreenstocks/assets/55627422/328efca4-bf0f-4d8b-9b7b-e0a02110b666)

This is the current window from where you will start your operations.

- **"Stock Ticker"** is for stock symbols (NETFLIX -> NFLX
- **"Amount"** only accepts int numbers, for the number of stocks you have
- **"Add Stock"** is to be pressed once you've succeddfully added a stock name and an amount
<br>
- **"Import Excel"** is a function that can be used if you have a Ptf to load following the example in "your_stock_example.xlsx" file
- **"Help"** can be used if you do not know the ticker of your stock 
- **"Finish"** MUST be pressed once you've finished using this window (even after loading an excel file) 


Once you press the "Finish" button, a Charging indicator will show on the screen until the code has finished. 
Two boxes are to be expected : 
![image](https://github.com/rletilly/Mygreenstocks/assets/55627422/74bdaa8f-a26c-4245-83c2-607620f3b241)

The most recent weighted ESG risk score of your portfolio. And 

![image](https://github.com/rletilly/Mygreenstocks/assets/55627422/95ae9957-30a0-46c9-aecb-0ba391c0e0f3)

The four most recent weighted grade of your Ptf.



