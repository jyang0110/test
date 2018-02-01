#Group C&A
#Lab one graph and GUI code
#Sources:
#videos from : https://www.youtube.com/user/sentdex and https://www.lynda.com
#tkinter documentation, matplotlib documentation
#other basic python guides and various stackoverflow posts

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import csv
import numpy as np
import urllib
import matplotlib.animation as animation
from matplotlib import style
import random
from tkinter import messagebox
from tkinter import *
from twilio.rest import Client

account_sid = "AC6b1f1bccd018165f0c10dd7de6a4a30d"
auth_token = "9297c36a3df5de99f27583112d74ee00"

LARGE_FONT = "Vernada", 20

SMALL_FONT = "Vernada", 15

win = tk.Tk()
win.wm_geometry("600x400")
win.title("Control Panel")
win.resizable(0,0)

frame = Frame(win)

Grid.rowconfigure(win,0,weight = 1)
Grid.columnconfigure(win,0,weight =1)

Grid.rowconfigure(win,1,weight =1)
Grid.columnconfigure(win,1,weight =1)


Grid.rowconfigure(win,2,weight =1)
Grid.columnconfigure(win,2,weight =1)


Grid.rowconfigure(win,3,weight =1)
Grid.columnconfigure(win,3,weight =1)


Grid.rowconfigure(win,4,weight =1)
Grid.columnconfigure(win,4,weight =1)


Grid.rowconfigure(win,5,weight =1)
Grid.columnconfigure(win,5,weight =1)
ctemp = ttk.Label(win, text="NA \u2103", font = LARGE_FONT,   foreground = 'red')
ctemp.grid(column=0, row=0)

#initial bounds of the graph
xmax=300
xmin=0
ymax=50
ymin=10


#make sure the data file is not empty, or may cause an error
#do so by padding end of file
y = np.loadtxt('//192.168.20.223/Public/datafile.txt',unpack=True)
fileData = open('datafile.txt','w')
for i in range(len(y)):
    fileData.write(str(y[i]))
    fileData.write('\n')
fileData.write("-100\n-100\n-100\n")
fileData.close()

#load LED file initially with LED off when program starts
fileLED = open('//192.168.20.223/Public/checkbutton.txt','w')
fileLED.write("False")
fileLED.close()

#code to test adding random data to the file
def addToFile(y):
    file = open('//192.168.20.223/Public/datafile.txt','w')
    file.write(str(random.randint(10,50)))
    file.write('\n')
    for i in range(len(y)):
        #print(y[i])
        file.write(str(y[i]))
        file.write('\n')
    file.close()

def sendMsg(number, msg):
    client = Client(account_sid, auth_token)
    
    client.api.account.messages.create(
    to= "+" + number,
    from_="+12252404150",
    body=msg)

#max range
def getMax():
    if maxRange.get()=='':
        return 100
    else:
        return int(maxRange.get())

#min range
def getMin():
    if minRange.get()=='':
        return -50
    else:
        return int(minRange.get())

def animate(i):
    #need to deal with possibility of y not being [] (only one val)
    y = np.loadtxt('//192.168.20.223/Public/datafile.txt',unpack=True)

    #check if data has been updated
    same=False
    #for i in range(min(len(y),len(lastData))):
     #   if lastData[i]!=y[i]:
      #      same=False
            
    #if hasn't been updated shift everything by one
    if(same):
        fileData = open('//192.168.20.223/Public/datafile.txt','w')
        fileData.write("-100\n")
        for i in range(len(y)):
            fileData.write(str(y[i]))
            fileData.write('\n')
        fileData.close()
        y = np.loadtxt('//192.168.20.223/Public/datafile.txt',unpack=True)
        
    #copy back over
    for i in range(min(len(y),len(lastData))):
        lastData[i]=y[i]

    #send txt message
    if(y[0]>-20 and len(phoneNumber.get())>=10):
        if minRange.get()!='':
            if int(minRange.get())>y[0] and (y[1]>=int(minRange.get()) or y[1]<-20):
                sendMsg(phoneNumber.get(), minRangeMessage.get())
        if maxRange.get()!='':
            if int(maxRange.get())<y[0] and y[1]<=int(maxRange.get()):
                sendMsg(phoneNumber.get(), maxRangeMessage.get())
    if(same):
         ctemp.configure(text = "no data available")
    elif(y[0] <=-20):
        ctemp.configure(text = "unplugged sensor")
    elif("\u2109" in switchUnits.cget("text")):
        ctemp.configure(text = str(y[0]) + "\u2103")
    else:
        ctemp.configure(text = str(y[0] * (9.0/5) + 32) + "\u2109")
        
    
    x = []
    #if more than 300 entries
    if(len(y)>300):
        y = y[0:299]
        #trim this here or in other program
        '''
        fileData = open('//192.168.20.223/Public/datafile.txt','w')
        for i in range(len(y)):
            fileData.write(str(y[i]))
            fileData.write('\n')
        fileData.close()
        '''
    #Hold limit zoomed in, but cannot zoom out further than original
    if ax1.get_xlim()[0]<=300:
        xmax=ax1.get_xlim()[0]
    else:
        xmax=100
    if ax1.get_xlim()[1] >= 0:
        xmin=ax1.get_xlim()[1]
    else:
        xmin=0
    if ax1.get_ylim()[1] <=63:
        ymax=ax1.get_ylim()[1]
    else:
        ymax=63
    if ax1.get_ylim()[0] >=-10:
        ymin=ax1.get_ylim()[0]
    else:
        ymin=-10
    ax1.clear()
    #trim for graph purposes
    i=0
    index=0
    brk = False
    while i < (len(y)):
        #or whatever condition signifying no data
        if y[i] >=-20: 
            if(brk == True):
                brk = False
                x=[]
                y=y[i:]
                i=0
            x.append(index)
            i=i+1
        else:
            if(brk == False):
                ax1.plot(x,y[0:len(x)],color='C0')
                brk = True
            y = np.delete(y,i)
        index = index +1
        
    #lines representing the bounds
    maxLine = np.empty(300)
    maxLine.fill(getMax())
    minLine = np.empty(300)
    minLine.fill(getMin())
    x1 = np.arange(len(maxLine))
    
    
    plt.xlabel('seconds ago from the current time')

    

    ax1.plot(x,y,color='C0')
    ax1.plot(x1,maxLine,color='red')
    ax1.plot(x1,minLine,color='red')
    
    plt.axis([xmin,xmax,ymin,ymax])
    #plt.xticks(np.arange(0,350,50))
    #plt.yticks(np.arange(-10,70,10))
    plt.gca().invert_xaxis()
    
    plt.ylabel('Temperature (\u2103)')
    plt.title('Thermometer Data')

#changes units from celcius to farenheit and vice versa
def changeUnits():
    if("\u2109" in switchUnits.cget("text")):
       switchUnits.configure(text = "Change to \u2103")
    else:
       switchUnits.configure(text = "Change to \u2109")

#changes the LED from being on to off and vice versa
def toggleLED():
    if displayLED.cget("text") == "Turn on LEDs":
        displayLED.configure(text = "Turn off LEDs", bg = "red")
        fileLED = open('//192.168.20.223/Public/checkbutton.txt','w')
        fileLED.write("True")
        fileLED.close()
    else:
        displayLED.configure(text = "Turn on LEDs", bg = "limegreen")
        fileLED = open('//192.168.20.223/Public/checkbutton.txt','w')
        fileLED.write("False")
        fileLED.close()
    #do something

#when window is closed
def closeProgram():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        fileLED = open('//192.168.20.223/Public/checkbutton.txt','w')
        fileLED.write("False")
        fileLED.close()
        win.destroy()
        plt.close()
        


maxRange = tk.StringVar()
maxEntry = ttk.Entry(win,width=3,textvariable = maxRange)
maxEntry.grid(column=1,row=1)
maxLabel = ttk.Label(win, text="max temp (\u2103)", font = SMALL_FONT)
maxLabel.grid(column=0,row=1)
maxRangeMessage = tk.StringVar()
maxMessageEntry = ttk.Entry(win, width = 30, textvariable = maxRangeMessage)
maxMessageEntry.grid(column=3, row=1)
maxMessageLabel = ttk.Label(win, text="message", font = SMALL_FONT)
maxMessageLabel.grid(column=2, row=1)

minRange = tk.StringVar()
minEntry = ttk.Entry(win,width=3,textvariable = minRange)
minEntry.grid(column=1,row=2)
minLabel = ttk.Label(win, text="min temp (\u2103)",font = SMALL_FONT)
minLabel.grid(column=0,row=2)
minRangeMessage = tk.StringVar()
minMessageEntry = ttk.Entry(win, width = 30, textvariable = minRangeMessage)
minMessageEntry.grid(column=3, row=2)
minMessageLabel = ttk.Label(win, text="message", font = SMALL_FONT)
minMessageLabel.grid(column=2, row=2)


phoneNumber = tk.StringVar()
phoneNumberEntry = ttk.Entry(win, width=10,textvariable=phoneNumber)
phoneNumberEntry.grid(column=1,row=3)
phoneLabel = ttk.Label(win, text="phone number",  font = SMALL_FONT)
phoneLabel.grid(column = 0, row = 3)

switchUnits = Button(win, text = "Change to \u2109",command = changeUnits, height = 2, width = 10)
switchUnits.grid(column=1, row=0)

displayLED = Button(win, text = "Turn on LEDs",command = toggleLED, bg = "limegreen", height = 2, width = 10)
displayLED.grid(column=1, row=4)


fig = plt.figure("Thermometer Graph")
lastData = np.empty(300)
lastData.fill(-40)
ax1 = fig.add_subplot(1,1,1)

plt.axis([xmin,xmax,ymin,ymax])
plt.gca().invert_xaxis()

ani = animation.FuncAnimation(fig,animate,interval=1000)
win.protocol("WM_DELETE_WINDOW",closeProgram)
plt.show()

win.mainloop()
