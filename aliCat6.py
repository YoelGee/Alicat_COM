import serial
import time
import keyboard
import ftd2xx as ft
# Set the COM port number
portName = 'COM5'
# Set the baud rate
baudRate = 19200
AliCat = 'B'
ftHandle = None
exit_key = 'q'
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G']  # Add more letters as needed
# Open the serial port
try:
    #ser = serial.Serial(portName, baudRate, timeout=1)  # Set timeout to 1 second
    print('Opened COM port: ' + portName)
    ftHandle = ft.open()
    print("FT_Open succeeded.")

except Exception as e:
    print("An exception occurred:", e)
    exit()
    
flowSet = 50
maxFlow = 500
adjustedFlowSet = (flowSet/maxFlow)*64000
# Send 'Hello' to start the program
ftHandle.write(f"\r\r{AliCat}{str(adjustedFlowSet)}\r".encode())
index = 0
while index < 2:
            # Get the current letter based on the index
            
    print(f"current Alicat: {AliCat}")
    ftHandle.write(f"{AliCat}\r".encode())
    bytes_to_read = 0
    while bytes_to_read < 64:
        bytes_to_read = ftHandle.getQueueStatus()
    if bytes_to_read > 0:
        data = ftHandle.read(bytes_to_read)
        print(data)
    if AliCat == 'A':
        AliCat = 'B'
    else:
        AliCat = 'A'  
            # Increment the index
    index += 1
        

#print("Data received:", read_data.decode('latin-1'))
if 'ftHandle' in locals():
    ftHandle.close()
    print("FT_Close succeeded.")
