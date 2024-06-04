import serial
import time
import keyboard
import ftd2xx as ft
import threading
import tkinter as tk
import pandas as pd
import csv
from datetime import datetime

class AliCatClass:
    def __init__(self, maxFlow, flowSet, ID):
        self.flowSet = flowSet
        self.maxFlow = maxFlow
        self.ID = ID

class HandleClass:
    def __init__(self, handler, *aliCats):
        self.handler = handler
        self.aliCats = aliCats
        self.running = None
        
    def read_until(self, str_term):
        chr = b''
        str = b''
        while chr.decode() != str_term:
            str = str + chr
            chr = self.handler.read(1)
        return str
            
    def set_flow(self):
        print(f"Initializing Alicat")
        #self.handler.write(b"\r\r")
        for aliCat in self.aliCats:
            if aliCat.ID in flow_rates:
                aliCat.flowSet = flow_rates[aliCat.ID]

                #self.handler.write(f"\r\r{aliCat.ID}0\r")
                time.sleep(0.1)
                print(f"setting flow for alicat {aliCat.ID}")
                adjusted_flow_set = (aliCat.flowSet / aliCat.maxFlow) * 64000
                self.handler.write(f"\r\r{aliCat.ID}{str(adjusted_flow_set)}\r".encode())
            
    def init_flow(self):   
        index = 0
        aliCat = self.aliCats[index]
        self.handler.write(f"{aliCat.ID}\r".encode())
        bytes_to_read = 0
        time.sleep(0.1)
        bytes_to_read = self.handler.getQueueStatus()
        if bytes_to_read > 0:
            data = self.handler.read(bytes_to_read)
            print(data)
            
    def read_flow(self):
        global new_flow, file_name
        index = 0
        counter = 0
        self.running = True

        while self.running:
            index = 0
            inuse = len(self.aliCats)
            if new_flow == True:
                self.set_flow()
                self.init_flow()
                new_flow = False
            while index < len(self.aliCats):
                    # Get the current aliCat
                    aliCat = self.aliCats[index]
                    
                    print(f"current Alicat: {aliCat.ID}")
                    self.handler.write(f"{aliCat.ID}\r".encode())
                    data = self.read_until('\r')
                    print(data)
                    current_datetime = datetime.now()
                    date_str = current_datetime.strftime("%Y-%m-%d")
                    time_str = current_datetime.strftime("%H:%M:%S")
                    full_data = f"{date_str} {time_str} {data.decode('utf-8')}"
                    split_data = full_data.split()
                    
                    log_data(file_name, split_data)
                    print(split_data)
                    
                    # Move to the next aliCat
                    index += 1
                    counter += 1
                    if counter == inuse:
                        counter = 0 
                        time.sleep(0.5)
    
    def stop(self):
        self.running = False

    

def save_values():
    global flow_rates, new_flow
    for i, entry in enumerate(entries):
        input_value = entry.get()
        if input_value.strip() == "":
            continue  # Skip if entry is blank
        try:
            flow_rate = float(input_value)
            if flow_rate < 0:
                raise ValueError("Flow rate cannot be negative")
            flow_rates[aliCats[i]] = flow_rate
        except ValueError as e:
            print(f"Error for Alicat {aliCats[i]}:", e)  
    new_flow = True
    print("Values saved:", flow_rates)
    

def close_window():
    global handler_instance
    handler_instance.stop()
    root.destroy()   

def create_csv_file(file_name):
    column_titles = ["Date", "Time", "UNIT ID", "PSIA", "temp C", "Volume (mL/s)", "Mass Flow", "SETPT", "Coumpound"]
    with open(file_name, 'w', newline='') as csv_file:
        # Your CSV writing code here, for example:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(column_titles)

    print(f"CSV file '{file_name}' created.")
    

def log_data(f_name, data):
    with open(f_name, 'a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(data)
    #folder_path = "csv_folder"

    

######################################################################################################################################


stop_thread = 'x'
exit_key = 'q'
new_flow = False
change_key = 'c'
MFCs_in_use = [0, 1, 2, 3, 4, 5, 6] 
aliCats = ['A','B', 'C', 'D', 'E', 'F', 'G']
max_flow_rates = [500, 500, 500, 500, 500, 500, 500]
file_name = None
    # Initialize flow rates dictionary
flow_rates = {key: 0 for key in aliCats}


######################################################################################################################################


def initialize_flow_rates():
    global flow_rates
    root = tk.Tk()
    root.title("Initial Flow Rate Input")
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    # Create entry widgets
    entries = []
    tk.Label(root, text='Set Initial Starting Set Points').grid(row=0, column=0, padx=5, pady=5)
    for i, ID in enumerate(aliCats):
        tk.Label(root, text=f'Alicat {ID}:').grid(row=i+1, column=0, padx=10, pady=10)
        entry = tk.Entry(root)
        entry.grid(row=i+1, column=1, padx=10, pady=10)
        entries.append(entry)

    # Save button
    def save_and_close():
        nonlocal root
        for i, entry in enumerate(entries):
            input_value = entry.get()
            if input_value.strip() == "":
                continue  # Skip if entry is blank
            try:
                flow_rate = float(input_value)
                if flow_rate < 0:
                    raise ValueError("Flow rate cannot be negative")
                flow_rates[aliCats[i]] = flow_rate
            except ValueError as e:
                print(f"Error for Alicat {aliCats[i]}:", e)
        print("Initial flow rates saved:", flow_rates)
        root.destroy()
        
    def close():
        nonlocal root
        root.destroy()
        exit()

    save_button = tk.Button(root, text="Save", command=save_and_close)
    save_button.grid(row=len(aliCats)+1, column=0, columnspan=2, padx=5, pady=10)
    
    close_button = tk.Button(root, text="Close", command=close)
    close_button.grid(row=len(aliCats)+1, column=1, columnspan=2, padx=5, pady=10)

    root.mainloop()


######################################################################################################################################
aliCat_objects = []

try:
    initialize_flow_rates()
    #print(aliCat_objects[0])

    #object1 = aliCat_objects[0]

    ser = serial.Serial("COM5", 19200)

    ser.close()
    
    current_time = datetime.now()
    time_str = current_time.strftime("%Y_%m_%d_%H_%M_%S")
    file_name = f"data_{time_str}.csv"
    create_csv_file(file_name)
    
    root = tk.Tk()
    root.title("Flow Rate Input")
    root.protocol("WM_DELETE_WINDOW", lambda: None)

    # Create entry widgets
    entries = []
    
    for i, ID in enumerate(aliCats):
        tk.Label(root, text=f'Alicat {ID}:').grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(root)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries.append(entry)
        #ftHandle.setTimeouts

    for index in MFCs_in_use:
        ID = aliCats[index]
        if ID in flow_rates:
            aliCat_objects.append(AliCatClass(max_flow_rates[index], flow_rates[ID], ID))

    ftHandle = ft.open()
    print(aliCat_objects[0])
    
    handler_instance = HandleClass(ftHandle, *aliCat_objects)
    
    handler_instance.set_flow()
    handler_instance.init_flow()
    
    read_flow_thread = threading.Thread(target=handler_instance.read_flow)
    read_flow_thread.start()
    
    # Save button
    save_button = tk.Button(root, text="Save", command=save_values)
    save_button.grid(row=len(aliCats), column=0, padx=5, pady=10)
    
    # Close button
    close_button = tk.Button(root, text="Close", command=close_window)
    close_button.grid(row=len(aliCats), column=1, padx=5, pady=10)
    
    root.mainloop()
except Exception as e:
    print("An exception occurred:", e)
    exit()
   
if 'ftHandle' in locals():
    ftHandle.close()
    print("FT_Close succeeded.")