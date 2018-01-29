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
#win.resizable(0,0)
ctemp = ttk.Label(win, text="NA \u2103", font = LARGE_FONT,   foreground = 'red')
ctemp.grid(column=0, row=0)

#make sure the data file is not empty, or may cause an error
#do so by padding end of file
y = np.loadtxt('data.txt',unpack=True)
fileData = open('data.txt','w')
for i in range(len(y)):
    #print(y[i])
    fileData.write(str(y[i]))
    fileData.write('\n')
fileData.write("-100\n-100\n-100\n")
fileData.close()

#load LED file initially with LED off when program starts
fileLED = open('LED.txt','w')
fileLED.write("OFF")
fileLED.close()

def addToFile(y):
    #temp = np.loadtxt('testing.txt',unpack=True)
    #print(temp)
    file = open('data.txt','w')
    file.write(str(random.randint(10,50)))
    file.write('\n')
    for i in range(len(y)):
        #print(y[i])
        file.write(str(y[i]))
        file.write('\n')
    file.close()

def getMax():
    if maxRange.get()=='':
        return 50
    else:
        return int(maxRange.get())
    #get value from gui

def getMin():
    if minRange.get()=='':
        return 0
    else:
        return int(minRange.get())
    #get value from gui

def animate(i):
    #need to deal with possibility of y not being [] (only one val)
    ax1.clear()
    y = np.loadtxt('data.txt',unpack=True)
    
    if(y[0]>-20 and len(phoneNumber.get())>=10):
        if minRange.get()!='':
            if int(minRange.get())>y[0] and (y[1]>int(minRange.get()) or y[1]<-20):
                #change to send txt message code instead of print
                print(minRangeMessage.get())
        if maxRange.get()!='':
            if int(maxRange.get())<y[0] and y[1]<int(maxRange.get()):
                #change to send txt message code instead of print
                print(maxRangeMessage.get())
    
    if(y[0] <=-20):
        ctemp.configure(text = "unplugged sensor")
    elif("\u2109" in switchUnits.cget("text")):
        ctemp.configure(text = str(y[0]) + "\u2103")
    else:
        ctemp.configure(text = str(y[0] * (9.0/5) + 32) + "\u2109")
        
    
    #print (y)
    x = []
    #addToFile(y)
    if(len(y)>300):
        y = y[0:299]
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
                #print(x)
            x.append(index)
            #print(x)
            i=i+1
        else:
            if(brk == False):
                #print(y[0:len(x)])
                #print(x)
                ax1.plot(x,y[0:len(x)],color='C0')
                brk = True
            y = np.delete(y,i)
        index = index +1
    
    maxLine = np.empty(300)
    maxLine.fill(getMax())
    minLine = np.empty(300)
    minLine.fill(getMin())
    x1 = np.arange(len(maxLine))
    #print (x)
    #print (y)
    ##print(x1)
    ##print (maxLine)
    ##print (minLine)
    ax1.plot(x,y,color='C0')
    ax1.plot(x1,maxLine,color='red')
    ax1.plot(x1,minLine,color='red')
    plt.xlabel('seconds ago from the current time')
    xmax=300
    xmin=0
    ymax=50
    ymin=10
    plt.axis([xmin,xmax,ymin,ymax])
    plt.xticks(np.arange(0,350,50))
    plt.yticks(np.arange(10,60,10))
    plt.gca().invert_xaxis()
    plt.ylabel('Temperature (\u2103)')
    plt.title('Thermometer Data')

    

'''
def getCurrentTemp():
    #get first value in file
    temp = 40
    if("\u2109" in switchUnits.cget("text")):
        return temp
    else:
        return temp * (9.0/5) + 32
'''

def changeUnits():
    if("\u2109" in switchUnits.cget("text")):
       #ctemp.configure(text = "\u2109")
       switchUnits.configure(text = "Change to \u2103")
    else:
       #ctemp.configure(text="\u2103")
       switchUnits.configure(text = "Change to \u2109")

def toggleLED():
    if displayLED.cget("text") == "Turn on LEDs":
        displayLED.configure(text = "Turn off LEDs", bg = "red")
        fileLED = open('LED.txt','w')
        fileLED.write("ON")
        fileLED.close()
    else:
        displayLED.configure(text = "Turn on LEDs", bg = "limegreen")
        fileLED = open('LED.txt','w')
        fileLED.write("OFF")
        fileLED.close()
    #do something

def closeProgram():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        fileLED = open('LED.txt','w')
        fileLED.write("OFF")
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

#ctemp.configure(text = str(getCurrentTemp()) + ctemp.cget("text"))

#setTemp = ttk.Button(win, text = "Set Range",command = setRange)
#setTemp.grid(column=1, row=4)

displayLED = Button(win, text = "Turn on LEDs",command = toggleLED, bg = "limegreen", height = 2, width = 10)
displayLED.grid(column=1, row=4)


fig = plt.figure("Thermometer Graph")

ax1 = fig.add_subplot(1,1,1)
ani = animation.FuncAnimation(fig,animate,interval=1000)
win.protocol("WM_DELETE_WINDOW",closeProgram)
#plt.protocol("Close Program", closeProgram)
plt.show()

win.mainloop()
