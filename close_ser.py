import ftd2xx as ft

ftHandle = ft.open()

if 'ftHandle' in locals():
    ftHandle.setRts()
    ftHandle.setDtr()
    ftHandle.close()
    print("FT_Close succeeded.")