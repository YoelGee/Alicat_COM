import serial
import time
import ftd2xx as ft
# Set the COM port number
portName = 'COM5'
flowSet = 200.0
maxFlow = 500.0
adjustedFlowSet = (flowSet/maxFlow)*64000

#print('Opened COM port: ' + portName)
ftHandle = ft.open(0)
#ftHandle.setBaudRate(19200)
#ftHandle.setTimeouts(1000, 5000)
ftHandle.write(b"\r\rB" + str(adjustedFlowSet).encode() + b"\r")
time.sleep(1)
#print(ftHandle.getEventStatus())
print("FT_Open succeeded.")
ftHandle.write(b'B\r')
time.sleep(1)
#print(ftHandle.getEventStatus())
bytes_to_read = ftHandle.getQueueStatus()
print(bytes_to_read)
if bytes_to_read > 0:
            # Read data from the device
    data = ftHandle.read(bytes_to_read)
    print(ftHandle.getEventStatus())
    time.sleep(1)
    print(data)
        # Close the FTDI device
if 'ftHandle' in locals():
    ftHandle.close()
    print("FT_Close succeeded.")

#print("Data received:", read_data.decode('latin-1'))

