# -*- coding: iso-8859-15 -*-
#required libs: urllib3, json
###########################imports#########################################
#import urllib3 to send request
import urllib3
#import tk for user interface
import tkinter as tk
#import json to be able to parse json responses
import json
#import qrcode to generate qr code from link
import qrcode
#import PIL for working with images
from PIL import Image, ImageTk
import os.path
#######################################################################

#define http for requests
http = urllib3.PoolManager()

#initalise array which always contains newest bills
billObjects = []

class WindowMain():
        
    def __init__(self):

        #location of get five newest of api merke http request sollte ein http:// vor den link -.-
        r = http.request('GET', "http://DESKTOP-UMN87KA:3000/get?auth=1234")

        #parse json file in array of Python dictionaries
        global billObjects
        billObjects = json.loads(r.data.decode('utf-8'))

        self.window = tk.Tk()
        self.window.grid()

        for i in range(0, len(billObjects)):
        # WaiterButton(frame, desc, identifier,row, col) Use object id as identifier                       
            WaiterButton(self.window, "Table " + str(billObjects[i]["tableNumber"]), billObjects[i]["_id"],i,2)


        # padx 20pixel from border
        self.window.ButtonGetList=tk.Button(self.window, text = 'Liste Anzeigen',height = 3,width = 20,
                                            command = self.btGetCompleteList).grid(column = 1, row = 3,padx=20)
        self.window.ButtonReload=tk.Button(self.window, text = 'Aktualisieren', height = 3, width = 20,
                                           command = self.btReloadWaiterList).grid(column = 3, row = 3,padx=20)
                                           

    def btGetCompleteList(self):
        print('Event: btGetCompleteList')
        
    def btReloadWaiterList(self):
        print('Event: Reload')
        self.destroyWindowMain()
        self.__init__()
        self.runWindowMain()

    def runWindowMain(self):
       
        self.window.title(" Rechnungen")
        # set hardcoded size of the window
        #self.window.geometry('800x480')
        self.window.mainloop()

    def destroyWindowMain(self):
        self.window.destroy()
        self.window.quit()

    def quitWindowMain(self):
        self.window.quit()
        exit()
#______________________________________________________________________________________________________-
class WindowSelectQRCodeOrPrint():
    def __init__(self):
        self.window=tk.Tk()
        self.window.grid()
        self.window.ButtonReturn = tk.Button(self.window, text = 'Zurück',command = self.btReturnToWindowMain, height = 3,width = 20).grid(row = 1, column = 1)
        self.window.ButtonShowQRCode = tk.Button(self.window, text = 'QR-Code anzeigen',command = self.btShowQRCode,  height = 20, width = 35).grid(row = 2, column = 2)
        self.window.ButtonPrint = tk.Button(self.window, text = 'Ausdrucken',command = self.btPrintBill, height = 20, width = 35).grid(row = 2, column = 3)

    def runWindowSelectQRCodeOrPrint(self,ipTischnr):

        self.sBillID=ipTischnr
        self.window.title("Auswahlmenu")
        # set hardcoded size of the window
        self.window.geometry('800x480')
        #self.window.mainloop()
        
    def destroyWindowSelectQRCodeOrPrint(self):
        self.window.destroy()

    def quitWindowSelectQRCodeOrPrint(self):
        self.window.quit()

    def btReturnToWindowMain(self):
        self.destroyWindowSelectQRCodeOrPrint()
        x = WindowMain()
        x.runWindowMain()
    def btShowQRCode(self):
        
        print('Event: btShowQRCode')
        
        # DB connection and class initialized on startup in __main__ 
        sDBOrderID=str(self.sBillID)
        for i in billObjects:
         if i["_id"] == sDBOrderID:
           authkey = i["randomAuthKey"]
           break


        #generate URL with random autkey as value
        sAPIHTTPURL= "http://DESKTOP-UMN87KA:3000/see/"+ str(sDBOrderID) + "?auth=" + authkey
        
        # print data on console_scripts
        print("Set URL to see bill to:" + str(sDBOrderID))
            
        self.destroyWindowSelectQRCodeOrPrint()
        x = WindowQRCode(sDBOrderID,sAPIHTTPURL)
        x.runFrameQrCode()
        
    def btPrintBill(self):
        print('Event: btPrintBill')
  
        sDBOrderID=self.sBillID
        
        for i in billObjects:
            print(i)
            if i["_id"] == sDBOrderID:
                print(i["boughtItems"])
                break
        updateDatabase(sDBOrderID)
    

        
        self.btReturnToWindowMain()

class WaiterButton():
    def __init__(self, master=None, pBtdesc=None, pBtNumber=None,pRow=None,pCol=None):
        self.master=master
        self.pBtNumber=pBtNumber
        bt=tk.Button(self.master, text=pBtdesc, height = 3,width = 20, command=self.btPressEvent).grid(row=pRow, column=pCol, pady=10,padx=60)

    def btPressEvent(self):
        # GetData from Database here
        self.master.destroy()
        x = WindowSelectQRCodeOrPrint()
        x.runWindowSelectQRCodeOrPrint(self.pBtNumber)
        print('Hallo button pressed:' + str(self.pBtNumber))
        
class WindowQRCode():
    def __init__(self,ipTischnr, sHTTPUrl):
        
        self.iTischnr=ipTischnr
       
        self.window = tk.Tk()
        # Creating an instance of QRCode class
        qr = qrcode.QRCode(version = 1,
                   box_size = 7,
                   border = 1)
  
        qr.add_data(sHTTPUrl)
  
        qr.make(fit = True)
        img = qr.make_image(fill_color = 'blue',
                    back_color = 'white')
  
        # image filename
        sQRFile="c:/temp/qrcode.png"               
        img.save(sQRFile)
      
        if (os.path.exists(sQRFile)==False):
            sError="ERROR - QRCode Datei nicht vorhanden und kann nicht geladen werden!"
            tk.Label(self.window, text=sError,bg="white",fg="red").grid(row=0,column=1, pady=10,padx=10)
            return
        
        #QR code For Testing Implemented here
        imgQRCode=tk.PhotoImage(file=sQRFile)
         
 
                        
        # Create image label to display the image
        lableQR=tk.Label(self.window,image=imgQRCode)
        lableQR.imgQRCode=imgQRCode
        # zeige logo an position 0,0 Frame an
        lableQR.place(x=250,y=75)
        #image1 = tk.PhotoImage(file = "C:\Program Files\TestCode.png")
        #label1 = tk.Label(self.window, image=image1).grid(row = 1, column = 1)
        #__________________________________________________
        self.window.ButtonReturn = tk.Button(self.window, text = 'Zurück',height = 3,width = 20, command = self.returnSelectQRCodeOrPrint).place(x = 250, y = 375)
        self.ButtonDone = tk.Button(self.window, text = 'Fertig',height = 3,width = 20, command =self.returnToMainMenu ).place(x = 400, y = 375)
        
    def returnToMainMenu(self):
        updateDatabase(self.iTischnr)
        self.window.destroy()
        # modified return to main after print or QR code scan
        # x = WindowSelectQRCodeOrPrint()
        # x.runWindowSelectQRCodeOrPrint(self.iTischnr)
        x = WindowMain()
        x.runWindowMain()
        
    def returnSelectQRCodeOrPrint(self):
        #fuer Datenbank: Rechnung bearbeitet gleich 1
        self.window.destroy()
        x = WindowSelectQRCodeOrPrint()
        x.runWindowSelectQRCodeOrPrint(self.iTischnr)
        
    def runFrameQrCode(self):
        self.window.title("QR-Code")
        # set hardcoded size of the window
        self.window.geometry('800x480')
        
        ###########################################
        # ERROR: self.window.mainloop()  not required
        #  -> when add loop still active
        #  -> memory leak application
        # self.window.mainloop()
        ###########################################
        
    def destroyWindowQRCode(self):
        self.window.destroy()
        self.window.quit()

    def quitWindowQRCode(self):
        self.window.destroy()
        self.window.quit()


def updateDatabase(billID):
    print("a request has been sent to http://DESKTOP-UMN87KA:3000/update/" + str(billID) + "?auth=1234")
    http.request("GET", "http://DESKTOP-UMN87KA:3000/update/" + str(billID) + "?auth=1234")


if __name__ == "__main__":
    x = WindowMain()
    x.runWindowMain()
