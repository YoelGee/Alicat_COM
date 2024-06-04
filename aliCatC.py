import serial
import time
import keyboard
import ftd2xx as ft
# Set the COM port number
  
class AliCatClass:
    def __init__(self, maxFlow, flowSet, ID):
        self.flowSet = flowSet
        self.maxFlow = maxFlow
        self.ID = ID

  

class HandleClass:
    def __init__(self, handler, *aliCats):
        self.handler = handler
        self.aliCats = aliCats

    def set_flow(self):
        print(f"Initializing Alicat")
        #self.handler.write(b"\r\r")
        for aliCat in self.aliCats:
            #self.handler.write(f"\r\r{aliCat.ID}0\r")
            time.sleep(0.5)
            print(f"setting flow for alicat{aliCat.ID}")
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
            
    def read_flow(self):
        index = 0
        counter = 0
        while True:
            if keyboard.is_pressed(exit_key):
                print("Exiting the loop.")
                break
            index = 0

            while index < len(self.aliCats):
                # Get the current aliCat
                aliCat = self.aliCats[index]
                
                print(f"current Alicat: {aliCat.ID}")
                self.handler.write(f"{aliCat.ID}\r".encode())
                bytes_to_read = 0
                while bytes_to_read < 46:
                    bytes_to_read = self.handler.getQueueStatus()
                if bytes_to_read > 0:
                    data = self.handler.read(bytes_to_read)
                    print(data.decode('utf-8'))
                
                
                # Move to the next aliCat
                index += 1
                counter += 1
                if counter == 7:
                    counter = 0 
                    time.sleep(1)

portName = 'COM5'
# Set the baud rate
baudRate = 19200
MFCs_in_use = ['A','B','C']
aliCats = ['A','B', 'C', 'D', 'E', 'F', 'G']
max_flow_rates = [10000, 500, 5000, 0, 0, 0]
initial_flow_rates = [0, 0, 0, 0, 0, 0]
ftHandle = None
exit_key = 'q'                    

try:
    ftHandle = ft.open()
    #ftHandle.setTimeouts(500, 500)

    AliA = AliCatClass(10000, 0, 'A')
    AliB = AliCatClass(500, 0, 'B')
    AliC = AliCatClass(5000, 0, 'C')
    handler_instance = HandleClass(ftHandle, AliA, AliB, AliC)
    handler_instance.set_flow()
    handler_instance.init_flow()
    handler_instance.read_flow()
    print("FT_Open succeeded.")

except Exception as e:
    print("An exception occurred:", e)
    exit()
   
if 'ftHandle' in locals():
    ftHandle.close()
    print("FT_Close succeeded.")
