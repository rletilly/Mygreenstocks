#####################################################################################################################################################################################################################
######################################################################### GUI - GRAPHICAL USER INTERFACE ############################################################################################################
#####################################################################################################################################################################################################################
import tkinter as tk
import time
import threading
from tkinter import *
from mygreenstocks import *

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
        animation_thread = threading.Thread(target=charging_animation)
        animation_thread.start()
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

def charging_animation():
    messages = ["Charging |", "Charging /", "Charging -", "Charging \\"]
    i = 0
    
    while not animation_stop_event.is_set():
        message = messages[i % len(messages)]  # Cycle through messages
        print(message, end="\r")  # Print message and move cursor to the beginning of the line
        time.sleep(0.5)  # Wait for a short duration (e.g., 0.5 seconds)
        i += 1

def main():
    global animation_stop_event
    animation_stop_event = threading.Event()
    add_stock_window()
    animation_stop_event.set()  # Signal the animation thread to stop
    print("The function is done.")

main()