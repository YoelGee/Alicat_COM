import ctypes

# Load the FTD2XX library
ftd2xx = ctypes.windll.ftd2xx

def count_connected_devices():
    # Create a buffer to hold device information
    num_devices = ctypes.c_ulong()

    # Call the FTD2XX library function to get the number of connected devices
    status = ftd2xx.FT_ListDevices(ctypes.byref(num_devices), None, ftd2xx.FT_LIST_NUMBER_ONLY)

    if status == 0:
        return num_devices.value
    else:
        return -1  # Error occurred

num_connected_devices = count_connected_devices()
if num_connected_devices >= 0:
    print("Number of connected FTDI devices:", num_connected_devices)
else:
    print("Error occurred while counting connected devices.")