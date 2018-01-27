import tkinter as tk
from tkinter import ttk
win = tk.Tk()
win.title("Thermometer")
#win.resizable(0,0)
ctemp = ttk.Label(win, text="\u2103")
ctemp.grid(column=0, row=0)

def getCurrentTemp():
    #get first value in file
    temp = 40
    if("\u2103" in ctemp.cget("text")):
        return temp
    else:
        return temp * (9.0/5) + 32

def changeUnits():
    if("\u2109" in switchUnits.cget("text")):
       ctemp.configure(text = "\u2109")
       switchUnits.configure(text = "Change to \u2103")
    else:
       ctemp.configure(text="\u2103")
       switchUnits.configure(text = "Change to \u2109")
    ctemp.configure(text = str(getCurrentTemp()) + ctemp.cget("text"))

def setRange():
    maxResult.configure(text="current max = " + maxRange.get())
    minResult.configure(text="current min = " + minRange.get())
    minEntry.delete(0,'end')
    maxEntry.delete(0,'end')
    #maxEntry.configure(text = "")

def displayLED():
    return 0
    #do something

ctemp.configure(text = str(getCurrentTemp()) + ctemp.cget("text"))

maxRange = tk.StringVar()
maxEntry = ttk.Entry(win,width=3,textvariable = maxRange)
maxEntry.grid(column=1,row=1)
maxLabel = ttk.Label(win, text="enter max temp")
maxLabel.grid(column=0,row=1)
maxResult = ttk.Label(win, text="")
maxResult.grid(column = 2, row=1)

minRange = tk.StringVar()
minEntry = ttk.Entry(win,width=3,textvariable = minRange)
minEntry.grid(column=1,row=2)
minLabel = ttk.Label(win, text="enter min temp")
minLabel.grid(column=0,row=2)
minResult = ttk.Label(win, text="")
minResult.grid(column = 2, row=2)


switchUnits = ttk.Button(win, text = "Change to \u2109",command = changeUnits)
switchUnits.grid(column=1, row=0)

setTemp = ttk.Button(win, text = "Set Range",command = setRange)
setTemp.grid(column=1, row=4)

displayLED = ttk.Button(win, text = "Display LED",command = displayLED)
displayLED.grid(column=1, row=5)

win.mainloop()
