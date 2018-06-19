from random import *
import time
import matplotlib.pyplot as plt

def mergeSort(file1):
    if len(file1)>1:
        mid = len(file1)//2
        lefthalf = file1[:mid]
        righthalf = file1[mid:]

        mergeSort(lefthalf)
        mergeSort(righthalf)

        i=0
        j=0
        k=0
        while i < len(lefthalf) and j < len(righthalf):
            if lefthalf[i] < righthalf[j]:
                file1[k]=lefthalf[i]
                i=i+1
            else:
                file1[k]=righthalf[j]
                j=j+1
            k=k+1

        while i < len(lefthalf):
            file1[k]=lefthalf[i]
            i=i+1
            k=k+1

        while j < len(righthalf):
            file1[k]=righthalf[j]
            j=j+1
            k=k+1
    return file1

def quicksort(file2):

    if not file2:
        return []

    pivots = [x for x in file2 if x == file2[0]]
    lesser = quicksort([x for x in file2 if x < file2[0]])
    greater = quicksort([x for x in file2 if x > file2[0]])

def insertionSort(file3):
    for i in range(1, len(file3)):
        retain = file3[i]
        j = i
        while j > 0 and file3[j - 1] > retain:
            file3[j] = file3[j - 1]
            j = j - 1
        file3[j] = retain

def decreasing(N):

    output = list(reversed(range(N)))
    #        print output
    return output

a=[]
b=[]
c=[]
d=[]
e=[]
f=[]

for x in range(50,1000,20):
    ourList = decreasing(x)
    #print ourList
    mergeList = ourList[:]
    timeStarted = time.time()
    mergeSort(mergeList)
    timeFinished = time.time()
    a.append(timeFinished-timeStarted)
    e.append(x)
#    print a,e,x

for y in range(50,1000,20):
    ourList = decreasing(y)
    InsertList = ourList[:]
    timeStarted = time.time()
    insertionSort(InsertList)
    timeFinished = time.time()
    b.append(timeFinished-timeStarted)
    c.append(y)
#    print b,c,y

for y in range(50,1000,20):
    ourList = decreasing(y)
    quickList = ourList[:]
    timeStarted = time.time()
    quicksort(quickList)
    timeFinished = time.time()
    d.append(timeFinished-timeStarted)
    f.append(y)
#    print b,c,y

plt.plot(e,a)
plt.plot(c,b)
plt.plot(f,d)

plt.ylabel('Number of seconds')
plt.xlabel('Number of Inputs')
plt.legend(['Blue = Mergesort','Orange = InsertionSort','Green = QuickSort'], loc='upper left')
plt.show()