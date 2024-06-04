import serial
import serial.tools.list_ports
# Define the device properties
vendor_id = 0x0403
product_id = 0x6001
serial_number = 'AU01I4ZEA'

# Find the port associated with the device
port = None
for p in serial.tools.list_ports.comports():
    if p.vid == vendor_id and p.pid == product_id and p.serial_number == serial_number:
        port = p.device
        break

# Open the serial port
if port:
    ser = serial.Serial(port, 19200)  # Adjust the baud rate as needed
    print(f"Serial port {port} opened successfully.")
    # Proceed with communication
else:
    print("Device not found or serial port could not be opened.")
    
flowSetA = 500
maxFlowA = 10000
adjustedFlowSetA = (flowSetA/maxFlowA)*64000

flowSetB = 1000
maxFlowB = 500
adjustedFlowSetB = (flowSetB/maxFlowB)*64000
# Send 'Hello' to start the program
ser.write(b"\r\rA" + str(adjustedFlowSetA).encode() + b"\r")
    # Get the number of bytes available in the receive queue

ser.write(b'A\r')

# Optionally, you can wait for a response
response = ser.readline().decode().strip()
print("Response:", response)

ser.close()