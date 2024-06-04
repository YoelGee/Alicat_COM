import tkinter as tk
from tkinter import ttk
import serial
import time
import keyboard
import ftd2xx as ft
import threading
import pandas as pd
import csv
from datetime import datetime



stop_thread = 'x'
exit_key = 'q'
new_flow = False
start = False
change_key = 'c'
MFCs_in_use = [0, 1, 2, 3, 4, 5, 6] 
aliCats = ['A','B', 'C', 'D', 'E', 'F', 'G']
max_flow_rates = [500, 500, 500, 500, 500, 500, 500]
file_name = None
flow_rates = {key: 0 for key in aliCats}
aliCat_objects = []

######################################################################################################################################

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MFC Controller")
        self.geometry("300x350")

        # Container to hold all frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.entries = []
        self.frames = {}

        for F in (StartPage, RunningPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        global start
        frame = self.frames[page_name]
        if page_name == 'RunningPage':
            start_event.set()
        frame.tkraise()

    def save_values(self):
        global flow_rates, new_flow
        for i, entry in enumerate(self.entries):
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
    
        
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Set Initial Flow Values")
        label.grid(row = 0, column = 1, pady=10)

        for i, ID in enumerate(aliCats):
            tk.Label(self, text=f'Alicat {ID}:').grid(row=i+1, column=0, padx=5, pady=5)
            entry = tk.Entry(self)
            entry.grid(row=i+1, column=1, padx=5, pady=5)
            controller.entries.append(entry)
            
        setValButton = ttk.Button(self, text="Set Values", command=controller.save_values)
        setValButton.grid(row=len(aliCats)+1, column=0, padx=10, pady=10, sticky="e")
        
        runButton = ttk.Button(self, text="Start Run", command=lambda: controller.show_frame("RunningPage"))
        runButton.grid(row=len(aliCats)+1, column=1, padx=10, pady=10)
        
        closeButton = ttk.Button(self, text = "Close", command = self.close)
        closeButton.grid(row=len(aliCats)+2, column=0, columnspan=2, padx=10, pady=10)
        
    def close(self):
        global handler_instance
        handler_instance.stop()
        self.controller.destroy() 

class RunningPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ttk.Label(self, text="Set Initial Flow Values")
        label.grid(row = 0, column = 1, pady=10)

        for i, ID in enumerate(aliCats):
            tk.Label(self, text=f'Alicat {ID}:').grid(row=i+1, column=0, padx=5, pady=5)
            entry = tk.Entry(self)
            entry.grid(row=i+1, column=1, padx=5, pady=5)
            controller.entries.append(entry)

        update = ttk.Button(self, text="Update Flow",
                            command= controller.save_values)
        update.grid(row = len(aliCats)+1, column = 0, columnspan=2, padx = 10, pady=10, sticky= "w")
        
                
        closeButton = ttk.Button(self, text = "Close", command = self.close)
        closeButton.grid(row=len(aliCats)+2, column=0, columnspan=2, padx=10, pady=10, sticky= "w" )
        
    def close(self):
        global handler_instance
        handler_instance.stop()
        self.controller.destroy() 
        
######################################################################################################################################

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
        self.keep_running = True  # Flag to control the thread
        
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

        while self.keep_running:  # Check flag before continuing
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
        self.keep_running = False  # Signal the thread to stop
        self.running = False

     

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

if __name__ == "__main__":
    start_event = threading.Event()

    app_thread = threading.Thread(target=lambda: MainApp().mainloop())
    app_thread.start()

    # Main thread waits for the start event to be set
    start_event.wait()
    
    try:
        ser = serial.Serial("COM5", 19200)
        ser.close()
        
        current_time = datetime.now()
        time_str = current_time.strftime("%Y_%m_%d_%H_%M_%S")
        file_name = f"data_{time_str}.csv"
        create_csv_file(file_name)
        
        start_event = threading.Event()
        entries = []

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
        
    except Exception as e:
        print("An exception occurred:", e)
        exit()
    
    if 'ftHandle' in locals():
        ftHandle.close()
        print("FT_Close succeeded.")
