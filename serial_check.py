import serial.tools.list_ports

# Get a list of available serial ports
ports = serial.tools.list_ports.comports()

# Print out the list of available ports
for port, desc, hwid in sorted(ports):
    print(f"{port}: {desc} [{hwid}]")