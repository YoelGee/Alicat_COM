import serial

# Open the serial port
ser = serial.Serial('/dev/ttyUSB0', 19200)  # Change '/dev/ttyUSB0' to your serial port

# Check if there is data available
if ser.in_waiting > 0:
    # Read the data
    data = ser.readline().decode().strip()  # Decode bytes to string and strip newline characters
    print("Received:", data)

# Close the serial port when done
ser.close()