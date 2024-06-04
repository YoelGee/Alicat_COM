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
while True:
    if keyboard.is_pressed(exit_key):
        print("Exiting the loop.")
        break 
    ftHandle.write(f"{AliCat}\r".encode())
    bytes_to_read = 0
    time.sleep(0.1)
        #print(bytes_to_read)
    bytes_to_read = ftHandle.getQueueStatus()
    if bytes_to_read > 0:
            # Read data from the device
        data = ftHandle.read(bytes_to_read)
        print(data.decode('utf-8'))
        if AliCat == 'A':
            AliCat = 'B'
        else:
            AliCat = 'A'
        #time.sleep(1)
        

#print("Data received:", read_data.decode('latin-1'))
if 'ftHandle' in locals():
    ftHandle.close()
    print("FT_Close succeeded.")
