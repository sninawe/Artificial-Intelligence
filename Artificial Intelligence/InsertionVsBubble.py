# Insertion Sort vs Bubble Sort example in Python

from random import *
import time
import matplotlib.pyplot as plt

def insertionSort(file1):
    for i in range(1, len(file1)):
        retain = file1[i]
        j = i
        while j > 0 and file1[j - 1] > retain:
            file1[j] = file1[j - 1]
            j = j - 1
        file1[j] = retain


def bubbleSort(file2):
    for num in range(len(file2) - 1 ):
        for i in range( len(file2) - 1  ):
            if (file2[i] > file2[i+1]):
                temp = file2[i]
                file2[i] = file2[i+1]
                file2[i+1] = temp
            i = i+1


#Generates a random list of numbers:
def randfile(N):
    rfile = []
    for x in range(N):
        rfile = rfile + [ randrange(1,N) ]

    return rfile

a=[]
b=[]
c=[]
for x in range(2000,51000,2000):
    ourList = randfile(x)

    #Run bubble, insertion, and merge sort on the same list of numbers:
    c.append(x)
    #print ourList
    #print("List length is:", ourList)
    averagetimeb = 0
    for avg in range(1,10):
        BubbleList = ourList[:]
        timeStarted = time.time()
        bubbleSort(BubbleList)
        timeFinished = time.time()
        averagetimeb = averagetimeb + (timeFinished-timeStarted)
#        print (timeFinished-timeStarted),averagetimeb

    averageb = averagetimeb/10
#    print averageb
    a.append(averageb)
#    print a

    averagetimea = 0
    for avg in range(1,10):
        InsertList = ourList[:]
        timeStarted = time.time()
        insertionSort(InsertList)
        timeFinished = time.time()
        averagetimea = averagetimea + (timeFinished-timeStarted)
#        print (timeFinished-timeStarted),averagetimea

    averagea = averagetimea/10
#    print averagea
    b.append(averagea)
#    print b

plt.plot(c,a)
plt.plot(c,b)
plt.ylabel('Number of seconds')
plt.xlabel('Number of Inputs')
plt.legend(['Blue = Bubblesort','Orange = InsertionSort'], loc='upper left')
plt.show()