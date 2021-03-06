# -*- coding: utf-8 -*-

#Group C&A
#Lab one graph and GUI code
#Sources:
#videos from : https://www.youtube.com/user/sentdex and https://www.lynda.com
#tkinter documentation, matplotlib documentation
#other basic python guides and various stackoverflow posts

import Tkinter as tk
import ttk
import matplotlib.pyplot as plt
import csv
import numpy as np
import urllib
import matplotlib.animation as animation
from matplotlib import style
import random
import tkMessageBox
from Tkinter import *
from twilio.rest import Client
import time
import paramiko
import socket

#not connected

connected = False


#Sending data from PC to raspberry Pi
def sendData(fileName):
    global t
    if isOpen():
        #t = paramiko.Transport('169.254.154.179','22')
        #t.connect(username = 'pi', password = '123')
        try:
            sftp = paramiko.SFTPClient.from_transport(t)
            remotepath=fileName
            local = "C:\\Users\\yangw\\Documents\\SD\\test\\"
            localpath= (local + fileName)
            sftp.put(localpath,remotepath)
        except:
            connected=False
        #t.close()

#Downloading data from raspberry Pi to PC
def downloadData(fileName):
    global t
    if isOpen():
        #t = paramiko.Transport('169.254.154.179','22')
        #t.connect(username = 'pi', password = '123')
        try:
            sftp = paramiko.SFTPClient.from_transport(t)
            remotepath=fileName
            local = 'C:\\Users\\yangw\\Documents\\SD\\test\\'
            localpath= (local + fileName)
            sftp.get(remotepath, localpath)
        except:
            connected=False
        #t.close()
    
def isOpen():
    global connected,t
    if connected==False:
        try:
            t = paramiko.Transport('169.254.154.179','22')
            t.connect(username = 'pi', password = '123')
        except:
            connected = False
            return False
    connected = True
    return True

account_sid = "AC6b1f1bccd018165f0c10dd7de6a4a30d"
auth_token = "9297c36a3df5de99f27583112d74ee00"


#check if open
connected = isOpen()


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
ctemp = ttk.Label(win, text=("NA " + u'\N{DEGREE SIGN}' + 'C'), font = LARGE_FONT,   foreground = 'red')
ctemp.grid(column=0, row=0)

#initial bounds of the graph according to requirements
xmax=300
xmin=0
ymax=50
ymin=10


#make sure the data file is not empty, or may cause an error
#do so by padding end of file
downloadData('savedData.txt')
y = np.loadtxt('savedData.txt',unpack=True)
fileData = open('savedData.txt','w')
for i in range (len(y)):
    fileData.write(str(y[i]))
    fileData.write('\n')
for i in range (300-len(y)):
    fileData.write(str(-100))
    fileData.write('\n')
fileData.close()

#load LED file initially with LED off when program starts
fileLED = open('checkbutton.txt','w')
fileLED.write("False")
fileLED.close()
sendData('checkbutton.txt')


    
#difference between current time and saved timestamp    
def getTimeDifference():
    currentTime = time.time()
    downloadData('time.txt')
    fileTime = np.loadtxt('time.txt',unpack=True)
    difference = int(currentTime - fileTime)
    return difference

#text message part
def sendMsg(number, msg):
    client = Client(account_sid, auth_token)
    
    client.api.account.messages.create(
    to= "+1" + number,
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

#graphing part
def animate(i):
    same=False
    downloadData('datafile.txt')
    data = np.loadtxt('datafile.txt',unpack=True)

    y = np.empty(300)
    for i in range (len(lastData)-1):
        y[i+1]=lastData[i]
    if (data>65): #data out of range
        y[0]=-100
    elif(getTimeDifference()>2 or (not isOpen())): # Data unavailable
        y[0]=-40
        same=True
    else:
        y[0]=data
        same=False
    #copy back over
    for i in range(min(len(y),len(lastData))):
        lastData[i]=y[i]
    
    #send text message
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
    elif((u'\N{DEGREE SIGN}' + 'F') in switchUnits.cget("text")):
        ctemp.configure(text = str(y[0]) + u'\N{DEGREE SIGN}' + 'C')
    else:
        ctemp.configure(text = (str(y[0] * (9.0/5) + 32)[:5]) + u'\N{DEGREE SIGN}' +'F')
        
    
    x = []
    #if more than 300 entries
    if(len(y)>300):
        y = y[0:299]
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
        #condition signifying no data
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
    plt.gca().invert_xaxis()
    
    plt.ylabel(('Temperature' + u'\N{DEGREE SIGN}' + 'C'))
    plt.title('Thermometer Data')

#changes units from celcius to farenheit and vice versa
def changeUnits():
    if('F' in switchUnits.cget("text")):
       switchUnits.configure(text = ("Change to" + u'\N{DEGREE SIGN}' + 'C'))
    else:
       switchUnits.configure(text = ("Change to" + u'\N{DEGREE SIGN}' + 'F'))

#changes the LED from being on to off and vice versa
def toggleLED():
    if displayLED.cget("text") == "Turn on LEDs":
        displayLED.configure(text = "Turn off LEDs", bg = "red")
        fileLED = open('checkbutton.txt','w')
        fileLED.write("True")
        fileLED.close()
        sendData('checkbutton.txt')
    else:
        displayLED.configure(text = "Turn on LEDs", bg = "limegreen")
        fileLED = open('checkbutton.txt','w')
        fileLED.write("False")
        fileLED.close()
        sendData('checkbutton.txt')

#when window is closed
def closeProgram():
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
        fileLED = open('checkbutton.txt','w')
        fileLED.write("False")
        fileLED.flush()
        fileLED.close()
        sendData('checkbutton.txt')
        fileData = open('savedData.txt','w')
        for i in range (len(lastData)):
            fileData.write(str(lastData[i]))
            fileData.write('\n')
        fileData.flush()
        fileData.close()
        sendData('savedData.txt')
        
        fileTime = open('time.txt','w')
        fileTime.write(str(time.time()))
        fileTime.flush()
        fileTime.close()
        sendData('time.txt')
        
        win.destroy()
        plt.close()
        


maxRange = tk.StringVar()
maxEntry = ttk.Entry(win,width=3,textvariable = maxRange)
maxEntry.grid(column=1,row=1)
maxLabel = ttk.Label(win, text=("max temp" + u'\N{DEGREE SIGN}' + 'C'), font = SMALL_FONT)
maxLabel.grid(column=0,row=1)
maxRangeMessage = tk.StringVar()
maxMessageEntry = ttk.Entry(win, width = 30, textvariable = maxRangeMessage)
maxMessageEntry.grid(column=3, row=1)
maxMessageLabel = ttk.Label(win, text="message", font = SMALL_FONT)
maxMessageLabel.grid(column=2, row=1)

minRange = tk.StringVar()
minEntry = ttk.Entry(win,width=3,textvariable = minRange)
minEntry.grid(column=1,row=2)
minLabel = ttk.Label(win, text=("min temp" + u'\N{DEGREE SIGN}' + 'C'),font = SMALL_FONT)
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
switchUnits = Button(win, text = ("Change to" + u'\N{DEGREE SIGN}' + "F"),command = changeUnits, height = 2, width = 10)
switchUnits.grid(column=2, row=0)

displayLED = Button(win, text = "Turn on LEDs",command = toggleLED, bg = "limegreen", height = 2, width = 10)
displayLED.grid(column=1, row=4)

fig = plt.figure("Thermometer Graph")
downloadData('savedData.txt')
savedData = np.loadtxt('savedData.txt',unpack=True)
difference = getTimeDifference()
lastData = np.empty(300)

if getTimeDifference()>3:
    
    for i in range (min(getTimeDifference(),300)):
        lastData[i]=-80
    for i in range (299 - difference):
        lastData[i+difference]=savedData[i]
else:
    for i in range (299):
        lastData[i]=savedData[i] 

ax1 = fig.add_subplot(1,1,1)

plt.axis([xmin,xmax,ymin,ymax])
plt.gca().invert_xaxis()

computerFactor=200 #how slow the computer is
ani = animation.FuncAnimation(fig,animate,interval=1000-computerFactor) #update once a second
win.protocol("WM_DELETE_WINDOW",closeProgram)
plt.show()

win.mainloop()
