#!/usr/bin/env python
import os
import sys
import ctypes
########################################################################
# D2XX definitions
def check(f):
    if f != 0:
        names = [
        "FT_OK",
        "FT_INVALID_HANDLE",
        "FT_DEVICE_NOT_FOUND",
        "FT_DEVICE_NOT_OPENED",
        "FT_IO_ERROR",
        "FT_INSUFFICIENT_RESOURCES",
        "FT_INVALID_PARAMETER",
        "FT_INVALID_BAUD_RATE",
        "FT_DEVICE_NOT_OPENED_FOR_ERASE",
        "FT_DEVICE_NOT_OPENED_FOR_WRITE",
        "FT_FAILED_TO_WRITE_DEVICE",
        "FT_EEPROM_READ_FAILED",
        "FT_EEPROM_WRITE_FAILED",
        "FT_EEPROM_ERASE_FAILED",
        "FT_EEPROM_NOT_PRESENT",
        "FT_EEPROM_NOT_PROGRAMMED",
        "FT_INVALID_ARGS",
        "FT_NOT_SUPPORTED",
        "FT_OTHER_ERROR"]
        raise IOError("Error: (status %d: %s)" % (f, names[f]))
########################################################################
# Main Program
#
# Implements simple GetComPortNumber example from D2XX programmers guide.
class D2XXTest(object):
    def __init__(self):
        #Load driver binaries
        if sys.platform.startswith('linux'):
            self.d2xx = ctypes.cdll.LoadLibrary("libftd2xx.so")
        elif sys.platform.startswith('darwin'):
            self.d2xx = ctypes.cdll.LoadLibrary("libftd2xx.1.1.0.dylib")
        else:
            self.d2xx = ctypes.windll.LoadLibrary("ftd2xx")
            print('D2XX library loaded OK')
            sys.stdout.flush()
            self.getCom()
    def getCom(self):
        #create FT Handle variable
        self.ftHandle = ctypes.c_void_p()
        #Open the first device on the system
        check(self.d2xx.FT_Open(0, ctypes.byref(self.ftHandle)))
        #com port number variable
        lComPortNumber = ctypes.c_long()
        #retrieve com # with FT_GetComPortNumber
        check(self.d2xx.FT_GetComPortNumber(self.ftHandle,
        ctypes.byref(lComPortNumber)))
        if lComPortNumber.value == -1:
            print("No Com Port Assigned")
        else:
            print("Com Port Number: %d" % lComPortNumber.value)
            #call FT_Close to close connection
            check(self.d2xx.FT_Close(self.ftHandle))
                
                
if __name__ == '__main__':
    print("===== Python D2XX Get Com Port =====")
    app = D2XXTest()