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
###***** maybe add boolens for operating system so when you try and open a device you
class D2XXTest(object):
    def __init__(self):
        #Load driver binaries
        if sys.platform.startswith('linux'):
            self.d2xx = ctypes.cdll.LoadLibrary("libftd2xx.so")
        elif sys.platform.startswith('darwin'):
            self.d2xx = ctypes.cdll.LoadLibrary("libftd2xx.1.1.0.dylib")
        else:
            self.d2xx = ctypes.windll.LoadLibrary("ftd2xx")
            print ("D2XX library loaded OK\n")
            sys.stdout.flush()
            #call example fucntion
            self.getDevInfoList()
    def getDevInfoList(self):
            #declare vairables needed in function
            numDevs = ctypes.c_long()
            check(self.d2xx.FT_CreateDeviceInfoList(ctypes.byref(numDevs)))
            print ("Number of devices is: %d" % (numDevs.value))
        # if there is at least one device connected
            if numDevs.value > 0:
                #obtain device info for all devices on the system
                for i in range (numDevs.value):
            #create FT Handle variable
                    ftHandleTemp = ctypes.c_long()
                    Flags = ctypes.c_long()
                    ID = ctypes.c_long()
                    Type = ctypes.c_long()
                    LocId = ctypes.c_long()
                    SerialNumber = ctypes.create_string_buffer(16)
                    Description = ctypes.create_string_buffer(64)
                    #call GetDeviceInfoDetail function to obtain device details
                    check(self.d2xx.FT_GetDeviceInfoDetail(i,
                    ctypes.byref(Flags),ctypes.byref(Type), ctypes.byref(ID), ctypes.byref(LocId),
                    ctypes.byref(SerialNumber), ctypes.byref(Description), ctypes.byref(ftHandleTemp)))
                    #print the device details
                    self.printDetails(i,Flags.value, Type.value, ID.value,
                    LocId.value, SerialNumber.value, Description.value, ftHandleTemp.value)
            else:
                #if no devices exit the program
                sys.exit()
    def printDetails(self,dev,flags,ty,i_d,locid,serial,desc,handle):
            print ("Dev: %d" % (dev))
            print (" Flags=0x%x" % (flags))
            print (" Type=0x%x" % (ty))
            print (" ID=0x%x" % (i_d))
            print (" LocId=0x%x" % (locid))
            print (" SerialNumber=%s" % (serial))
            print (" Description=%s" % (desc))
            print (" ftHandle=0x%s" % (handle))
            
if __name__ == '__main__':
    print ("===== Python D2XX Get Device Info Detail =====\n")
    app = D2XXTest()