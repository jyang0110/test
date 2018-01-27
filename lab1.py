import matplotlib.pyplot as plt
import csv

x = []
y= [3,5,6,10,11]

with open('testing.txt','r') as csvfile:
    plots = csv.reader(csvfile)
    for row in plots:
        x.append(row[0])


plt.plot(x,y,label = 'test')

plt.xlabel('x')
plt.ylabel('y')
plt.title('lol')
plt.legend()
plt.show()
