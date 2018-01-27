import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import csv
import numpy as np
import urllib
import matplotlib.animation as animation
from matplotlib import style
import random

from tkinter import *

LARGE_FONT = "Vernada", 20

SMALL_FONT = "Vernada", 15

win = tk.Tk()
win.wm_geometry("400x400")
win.title("Thermometer")

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



# win.resizable(0,0)
ctemp = ttk.Label(win, text="\u2103", font = LARGE_FONT,   foreground = 'red')
ctemp.grid(column=0, row=0)



def addToFile(y):
    # temp = np.loadtxt('testing.txt',unpack=True)
    # print(temp)
    file = open('testing.txt', 'w')
    file.write(str(random.randint(10, 50)))
    file.write('\n')
    for i in range(len(y)):
        # print(y[i])
        file.write(str(y[i]))
        file.write('\n')
    file.close()


def getMax():
    if maxRange.get() == '':
        return 50
    else:
        return int(minRange.get())
    # get value from gui


def getMin():
    if maxRange.get() == '':
        return 0
    else:
        return int(minRange.get())
    # get value from gui


def animate(i):
    # need to deal with possibility of y not being [] (only one val)
    ax1.clear()
    y = np.loadtxt('testing.txt', unpack=True)
    # print (y)
    x = []
    addToFile(y)
    if (len(y) > 300):
        y = y[0:299]
    i = 0
    index = 0
    brk = False
    while i < (len(y)):
        # or whatever condition signifying no data
        if y[i] >= -20:
            if (brk == True):
                brk = False
                x = []
                y = y[i:]
                i = 0
                # print(x)
            x.append(index)
            # print(x)
            i = i + 1
        else:
            if (brk == False):
                # print(y[0:len(x)])
                # print(x)
                ax1.plot(x, y[0:len(x)], color='C0')
                brk = True
            y = np.delete(y, i)
        index = index + 1

    maxLine = np.empty(300)
    maxLine.fill(getMax())
    minLine = np.empty(300)
    minLine.fill(getMin())
    x1 = np.arange(len(maxLine))
    # print (x)
    # print (y)
    ##print(x1)
    ##print (maxLine)
    ##print (minLine)
    ax1.plot(x, y, color='C0')
    ax1.plot(x1, maxLine, color='red')
    ax1.plot(x1, minLine, color='red')
    plt.xlabel('seconds ago from the current time')
    xmax = 300
    xmin = 0
    ymax = 50
    ymin = 10
    plt.axis([xmin, xmax, ymin, ymax])
    plt.xticks(np.arange(0, 350, 50))
    plt.yticks(np.arange(10, 60, 10))
    plt.gca().invert_xaxis()
    plt.ylabel('Temperature (\u2103)')
    plt.title('Thermometer Data')


def getCurrentTemp():
    # get first value in file
    temp = 40
    if ("\u2103" in ctemp.cget("text")):
        return temp
    else:
        return temp * (9.0 / 5) + 32


def changeUnits():
    if ("\u2109" in switchUnits.cget("text")):
        ctemp.configure(text="\u2109")
        switchUnits.configure(text="Change to \u2103")
    else:
        ctemp.configure(text="\u2103")
        switchUnits.configure(text="Change to \u2109")
    ctemp.configure(text=str(getCurrentTemp()) + ctemp.cget("text"))


def setRange():
    maxResult.configure(text="current max = " + maxRange.get(), font = SMALL_FONT)
    minResult.configure(text="current min = " + minRange.get(), font = SMALL_FONT)
    minEntry.delete(0, 'end')
    maxEntry.delete(0, 'end')
    # maxEntry.configure(text = "")


def displayLED():
    return 0
    # do something


ctemp.configure(text=str(getCurrentTemp()) + ctemp.cget("text"))

maxRange = tk.StringVar()
maxEntry = ttk.Entry(win, width=3, textvariable=maxRange)
maxEntry.grid(column=1, row=1)
maxLabel = ttk.Label(win, text="enter max temp", font = SMALL_FONT)
maxLabel.grid(column=0, row=1)
maxResult = ttk.Label(win, text="")
maxResult.grid(column=2, row=1)

minRange = tk.StringVar()
minEntry = ttk.Entry(win, width=3, textvariable=minRange)
minEntry.grid(column=1, row=2)
minLabel = ttk.Label(win, text="enter min temp", font = SMALL_FONT)
minLabel.grid(column=0, row=2)
minResult = ttk.Label(win, text="")
minResult.grid(column=2, row=2)

switchUnits = ttk.Button(win, text="Change to \u2109", command=changeUnits)
switchUnits.grid(column=1, row=0)

setTemp = ttk.Button(win, text="Set Range", command=setRange)
setTemp.grid(column=1, row=4)

displayLED = ttk.Button(win, text="Display LED",  command=displayLED)
displayLED.grid(column=1, row=5)



fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()

win.mainloop()
