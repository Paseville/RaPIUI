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
from PIL import *
import os.path
#import datetime to get current date
import datetime

## #########################init printer#########################
import serial
import adafruit_thermal_printer
global printer 
global ThermalPrinter
global uart
#initalise array which always contains newest bills
global completeBillList
global billObjects
#Uncommment lines if on PI
uart = serial.Serial("/dev/serial0", baudrate=19200, timeout=3000)
ThermalPrinter = adafruit_thermal_printer.get_printer_class(2.69)
printer = ThermalPrinter(uart, auto_warm_up=False)
printer.warm_up()
notPrint = False
######################################################
#define http for requests
http = urllib3.PoolManager()
#define Variables
global SEE_URL
global GET_URL
global GETALL_URL
global UPDATE_URL
SEE_URL = "https://billgatesprojekt.herokuapp.com/see/"
API_KEY = "1234"
GET_URL =  "https://billgatesprojekt.herokuapp.com/get?auth=1234"
UPDATE_URL = "https://billgatesprojekt.herokuapp.com/update/"
GETALL_URL = "https://billgatesprojekt.herokuapp.com/get-all?auth=1234"


#define http for requests
class WindowMain():
        
    def __init__(self):
            global billObjects
            self.window = tk.Tk()
            self.formattingFrame = tk.Frame(self.window)
            self.formattingFrame.grid()
            #getNewData Returns 0 if an exception was thrown
            if (getNewData() != 0):
                #Check if Database is online and if there are any bills in it
                if (billObjects != []):
                    for i in range(0, len(billObjects)):
                        # WaiterButton(frame, desc, identifier,row, col) Use object id as identifier                       
                        WaiterButton(self.formattingFrame, "Table " + str(billObjects[i]["tableNumber"]), billObjects[i]["_id"],i,2,self.window)
                        placeOnWindow(self.window, self.formattingFrame)

                else:
                      w = tk.Label(self.formattingFrame, text = "No Bills found or Database not online")
                      w.grid(column = 2, row = 3)
                # padx 20pixel from border
                self.formattingFrame.ButtonGetList=tk.Button(self.formattingFrame, text = 'Liste Anzeigen',height = 3,width = 20,
                                                    command = self.btGetCompleteList,).grid(column = 1, row = 3,padx=20)
                self.formattingFrame.ButtonReload=tk.Button(self.formattingFrame, text = 'Aktualisieren', height = 3, width = 20,
                                                   command = self.btReloadWaiterList).grid(column = 3, row = 3,padx=20)
                placeOnWindow(self.window, self.formattingFrame)
                #Display Connection failed label and a Retry Button
            else:
                self.formattingFrame.btRetry=tk.Button(self.formattingFrame, text = 'Erneut Versuchen', command = self.fctBtRetry)
                self.formattingFrame.btRetry.place(anchor="c", relx=.5, rely=.5)
                errorLabel = tk.Label(self.formattingFrame, text = "No Bills found or Database not online")
                errorLabel.place(anchor="c", relx=.5, rely=.5)
                placeOnWindow(self.window, self.formattingFrame)
                                           

    def btGetCompleteList(self):
        self.destroyWindowMain()
        x = CompleteListWindow()
        x.runCompleteListWindow()
        
    def btReloadWaiterList(self):
        print('Event: Reload')
        self.destroyWindowMain()
        self.__init__()
        self.runWindowMain()

    def runWindowMain(self):
       
        self.window.title(" Rechnungen")
        # set hardcoded size of the window
        self.window.attributes("-fullscreen", True)
        self.window.mainloop()

    def destroyWindowMain(self):
        self.window.destroy()
        self.window.quit()

    def quitWindowMain(self):
        self.window.quit()
        exit()

    def fctBtRetry(self):
        self.destroyWindowMain()
        self.__init__()
        self.runWindowMain()
#______________________________________________________________________________________________________-
class WindowSelectQRCodeOrPrint():
    def __init__(self):
        self.window=tk.Tk()
        self.formattingFrame = tk.Frame(self.window)
        self.formattingFrame.grid()
        self.formattingFrame.ButtonReturn = tk.Button(self.formattingFrame, text = 'Zurück',command = self.btReturnToWindowMain, height = 3,width = 20).grid(row = 1, column = 1)
        self.formattingFrame.ButtonShowQRCode = tk.Button(self.formattingFrame, text = 'QR-Code anzeigen',command = self.btShowQRCode,  height = 20, width = 35).grid(row = 2, column = 2)
        self.formattingFrame.ButtonPrint = tk.Button(self.formattingFrame, text = 'Ausdrucken',command = self.btPrintBill, height = 20, width = 35).grid(row = 2, column = 3)
        placeOnWindow(self.window, self.formattingFrame)

    def runWindowSelectQRCodeOrPrint(self,ipTischnr):

        self.sBillID=ipTischnr
        self.window.title("Auswahlmenu")
        # set hardcoded size of the window
        self.window.attributes("-fullscreen", True)
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
        global completeBillList
        print('Event: btShowQRCode')
        #go thought short array first if id not found there search complete list array
        sDBOrderID=str(self.sBillID)
        found = 0
        for i in billObjects:
            if i["_id"] == sDBOrderID:
                found = 1
                authkey = i["randomAuthKey"]
                break
        if (found == 0):
            for i in completeBillList:
                if i["_id"] == sDBOrderID:
                    authkey = i["randomAuthKey"]
                    break 




        #generate URL with random autkey as value
        sAPIHTTPURL= SEE_URL + str(sDBOrderID) + "?auth=" + authkey
        
        # print data on console_scripts
        print("Set URL to see bill to:" + str(sDBOrderID))
            
        self.destroyWindowSelectQRCodeOrPrint()
        x = WindowQRCode(sDBOrderID,sAPIHTTPURL)
        x.runFrameQrCode()
        
    def btPrintBill(self):
        global completeBillList
        PrinterPrint(self.sBillID)
        #PrinterPrint(self.sBillID) 
        self.btReturnToWindowMain()

class WaiterButton():
    def __init__(self, master=None, pBtdesc=None, pBtNumber=None,pRow=None,pCol=None, windowMain=None):
        self.master=master
        self.windowMain = windowMain
        self.pBtNumber=pBtNumber
        bt=tk.Button(self.master, text=pBtdesc, height = 3,width = 20, command=self.btPressEvent).grid(row=pRow, column=pCol, pady=10,padx=60)

    def btPressEvent(self):
        # GetData from Database here
        self.windowMain.destroy()
        x = WindowSelectQRCodeOrPrint()
        x.runWindowSelectQRCodeOrPrint(self.pBtNumber)
        print('button pressed:' + str(self.pBtNumber))
        
class WindowQRCode():
    def __init__(self,ipTischnr, sHTTPUrl):
        
        self.iTischnr=ipTischnr
        self.window = tk.Tk()
        self.formattingFrame = tk.Frame(self.window, width = 800, height = 480)
        self.formattingFrame.grid()
        self.buttonFrame=tk.Frame(self.formattingFrame)
        # Creating an instance of QRCode class
        qr = qrcode.QRCode(version = 1,
                   box_size = 7,
                   border = 1)
  
        qr.add_data(sHTTPUrl)
  
        qr.make(fit = True)
        img = qr.make_image(fill_color = 'blue',
                    back_color = 'white')
  
        # image filename
        sQRFile = "/home/pi/Desktop/qrcode.png"            
        img.save(sQRFile)
      
        if (os.path.exists(sQRFile)==False):
            sError="ERROR - QRCode Datei nicht vorhanden und kann nicht geladen werden!"
            tk.Label(self.window, text=sError,bg="white",fg="red").grid(row=0,column=1, pady=10,padx=10)
            return
        
        #QR code For Testing Implemented here
       
        imgQRCode=tk.PhotoImage(file=sQRFile, master = self.formattingFrame)
         
 
                     
        # Create image label to display the image
        lableQR=tk.Label(master = self.formattingFrame,image=imgQRCode)
        lableQR.imgQRCode=imgQRCode
        # zeige logo an position 0,0 Frame an
        lableQR.pack(side="top")
        #image1 = tk.PhotoImage(file = "C:\Program Files\TestCode.png")
        #label1 = tk.Label(self.window, image=image1).grid(row = 1, column = 1)
        #__________________________________________________
        self.window.ButtonReturn = tk.Button(self.buttonFrame ,text = 'Zurück',height = 3,width = 20, command = self.returnSelectQRCodeOrPrint).pack(side="left")
        self.ButtonDone = tk.Button(self.buttonFrame, text = 'Fertig',height = 3,width = 20, command =self.returnToMainMenu ).pack(side="right")
        self.buttonFrame.pack(side="bottom")
        placeOnWindow(self.window, self.formattingFrame)
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
        self.window.attributes("-fullscreen", True)
        
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

class CompleteListWindow():
    def __init__(self):
        self.window = tk.Tk()
        self.formattingFrame = tk.Frame(self.window, width = 800, height = 480)
        self.formattingFrame.grid()
        self.buttonFrame = tk.Frame(self.formattingFrame)
        self.liboxFrame = tk.Frame(self.formattingFrame)
        global completeBillList
        #get complete List from Database
        if(getAllData() != 0):
            #create scrollbar for listbox
            
            
            
            #create list for items and link scrollbar to it
            self.liBox = tk.Listbox(self.liboxFrame, selectmode = tk.SINGLE)
            self.scrollBar = tk.Scrollbar(self.liboxFrame, orient="vertical")
            self.scrollBar.pack(side="right",fill="y")
            self.liBox.config(yscrollcommand=self.scrollBar.set)
            #get todays date as string
            t = datetime.datetime.now()
            rightTimetoCompare = t - datetime.timedelta(hours=2)
            dateToday = rightTimetoCompare.strftime("%Y-%m-%d")
            #add elements to listBox
            for i in completeBillList:
                print(i["created_at"][0:10])
                print(dateToday)
                if (dateToday[0:10] == i["created_at"][0:10]): #0:10 that only date is compared and not time
                    aSplitted = i["created_at"][11:16].split(":")
                    iHours = int(aSplitted[0])
                    iMinutes = int(aSplitted[1])
                    iHours += 2
                    stringToDisplay =  "Tisch " + str(i["tableNumber"]) + " Time : " + str(iHours) + ":" + str(iMinutes)
                    self.liBox.insert(tk.END, stringToDisplay)
            self.liBox.pack(side="left")
           
            #create Return Button
            self.buttonReturn = tk.Button(self.buttonFrame, text = 'Zurück',height = 3,width = 20, command = self.returnToMainMenu)
            self.buttonReturn.pack(side="left")
            #add Button for Selecting the currently marked Bill
            self.selBtn = tk.Button(self.buttonFrame, text = "Bestätigen",height = 3,width = 20, command = self.selectElement)
            self.selBtn.pack(side="right")
            self.buttonFrame.pack(side="bottom")
            self.liboxFrame.pack(side="top")
            placeOnWindow(self.window, self.formattingFrame)
        else:
            self.formattingFrame.btRetry=tk.Button(self.window, text = 'Erneut Versuchen', command = self.fctBtRetry)
            self.formattingFrame.btRetry.pack()
            errorLabel = tk.Label(self.window, text = "No Bills found or Database not online")
            errorLabel.pack()
            placeOnWindow(self.window, self.formattingFrame)
       
    def runCompleteListWindow(self):
        self.window.title(" Rechnungen")
        # set hardcoded size of the window
        self.window.attributes("-fullscreen", True)
        self.window.mainloop()

    def returnToMainMenu(self):
        self.window.destroy()
        self.window.quit()
        x = WindowMain()
        x.runWindowMain()

    def fctBtRetry(self):
        self.window.destroy()
        self.window.quit()
        self.__init__()
        self.runCompleteListWindow()

    def selectElement(self):
        selected = self.liBox.curselection()
        if selected: # only do stuff if user made a selection
            billID = completeBillList[int(selected[0])]["_id"] # get id of currently selected Table
            x = WindowSelectQRCodeOrPrint()
            x.runWindowSelectQRCodeOrPrint(billID)
            self.window.destroy()
            self.window.quit()


def updateDatabase(billID):
    print("a request has been sent to https://billgatesprojekt.herokuapp.com/update/" + str(billID))
    http.request("GET", UPDATE_URL + str(billID) + "?auth="+ API_KEY)

def daytime():

    today = datetime.date.today()
    now = datetime.datetime.now()
    dt_string = today.strftime("%d-%m-%Y")
    now_string = now.strftime("%H:%M:%S")
    todays_time = dt_string + '             ' + now_string
    return todays_time

def PrinterStart():
    ## Statt Konsolenausgabe hier ein Label auf fenster
    printer = False

    if printer:
        print("Printer has paper!")
    else:
        print("No Paper, or RX is disconnected!")
        global NotPrint
        NotPrint = True


#prints bill with billID (searches both arrays from database completeArray and billObjects)
def PrinterPrint(billID):
    #print(NotPrint)
    Bill = []
    global printer 
    global ThermalPrinter
    global completeBillList
    global uart
    global billObjects
    # not NotPrint

    printer.print('Bill Gate`(s)\nGasthaus')

    printer.print('-------------------------------\nStr. Adolf-Ley-Straße Nr.6\nPLZ: 97424 Stadt: Schweinfurt\nTel. 0972128704')

    printer.print('Rechnung')

    printer.print(daytime())
    printer.print('Bon.Nr.                Device 1\n-------------------------------\nBezeichnung Einzel Menge Gesamt\n-------------------------------')

    # Items printed
    
    
    sDBOrderID = billID
    found = 0
    print(billObjects)
    #Go through small array first to find bill, if not in there search big array
    for i in billObjects:
        print(sDBOrderID)
        print(i["_id"])
        if (i['_id'] == sDBOrderID):
            found = 1
            Bill = i
            updateDatabase(sDBOrderID)
            for x in Bill['boughtItems']:
                Pay = str(Bill['totalBill']) + "$"
                printer.print(adjustFormatting)
                # print(adjustFormatting(x))
            break
    if (found == 0):
        global completeBillList
        for i in completeBillList:
            if i["_id"] == sDBOrderID:
                Bill = i
                for x in Bill['boughtItems']:
                   printer.print(adjustFormatting(x))
                break
    #printer.print("\nTischnummer: " + str(Bill['tableNumber']))
    printer.print(Pay.rjust(31) )
    #printer.print("\nBezahlt: " + "{:.2f}".format(Bill["totalBill"]))

    # printed text 
    #printer.print("Es bedient: " + Bill['waiter'] + " Vielen Dank fuer Ihren Besuch!")

def adjustFormatting(Item):
                 name = Item['itemName']
                 price = str(Item['itemPriceOne']) + "$"
                 count = str(Item['itemsBought'])
                 total= str(Item['itemPriceAll'])+ "$"
                 #ljust for formatting the bill
                 #format to display orderly to display the corresponding decimal places under each other
                 if (len(str(Item['itemPriceOne'])) == 1):
                     name = name.ljust(16)
                 elif (len(str(Item['itemPriceOne'])) == 2):
                     name = name.ljust(15)
                 elif (len(str(Item['itemPriceOne'])) == 3):
                     name = name.ljust(14)
                 else:
                     name = name.ljust(13) #13 was normall before formatting
                 
                 #Now do the same for the total
                 count = count.rjust(6)
                 total = total.rjust(7)
                 completeLine = name + price  + count  + total
                 return completeLine
def getNewData():
    global billObjects
    #initalise array which always contains newest bills
    billObjects = []
    try:
        r = http.request('GET', GET_URL)
        billObjects = json.loads(r.data.decode('utf-8'))
        return 1
    except:
        return 0
def getAllData():
      
    global completeBillList
    try:
        r = http.request('GET', GETALL_URL)
        completeBillList = json.loads(r.data.decode('utf-8'))
        return 1
    except:
        return 0
def placeOnWindow(masterWindow, childWindow):
    childWindow.place(in_=masterWindow, anchor="c", relx=.5, rely = .5)
 
if __name__ == "__main__":
    x = WindowMain()
    x.runWindowMain()
