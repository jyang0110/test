import matplotlib.pyplot as plt
import csv
import numpy as np
import urllib
import matplotlib.animation as animation
from matplotlib import style
import random

'''
y = []
with open('C:\\Users\\yangw\\seniorDesign\\test\\testing.txt','r') as file:
    plots = csv.reader(file)
    for row in plots:
        y.append(row[0])
'''
def addToFile(y):
    #temp = np.loadtxt('testing.txt',unpack=True)
    #print(temp)
    file = open('testing.txt','w')
    file.write(str(random.randint(10,50)))
    file.write('\n')
    for i in range(len(y)):
        #print(y[i])
        file.write(str(y[i]))
        file.write('\n')
    file.close()

def getMax():
    return 40
    #get value from gui
def getMin():
    return 20
    #get value from gui

def animate(i):
    #need to deal with possibility of y not being [] (only one val)
    ax1.clear()
    y = np.loadtxt('testing.txt',unpack=True)
    #print (y)
    x = []
    addToFile(y)
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
    plt.ylabel('Temperature (Celcius)')
    plt.title('Thermometer Data')

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
ani = animation.FuncAnimation(fig,animate,interval=1000) 
plt.show()
