import serial
import time

import ftd2xx as ft
# Set the COM port number
portName = 'COM5'
# Set the baud rate
baudRate = 19200
ftHandle = None
AliCat = 'B'

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
maxFlow = 10000
adjustedFlowSet = (flowSet/maxFlow)*64000
# Send 'Hello' to start the program
# ftHandle.write(f"\r\rB{adjustedFlowSet}\r".encode())
# ftHandle.write(b'A\r')
def get_data(ID):
    ftHandle.write(f'{ID}\r'.encode())
    time.sleep(1)
    bytes_to_read = 0
    bytes_to_read = ftHandle.getQueueStatus()
    print(bytes_to_read)
    if bytes_to_read > 0:
            # Read data from the device
        data = ftHandle.read(bytes_to_read)
        print(data.decode('utf-8'))

def set_flow(ID):
    ftHandle.write(f"\r\r{ID}{adjustedFlowSet}\r".encode())
    time.sleep(1)

get_data(AliCat)
#print("Data received:", read_data.decode('latin-1'))
if 'ftHandle' in locals():
    ftHandle.close()
    print("FT_Close succeeded.")
