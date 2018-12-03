
#for extracting data from .ods
import re
from pyexcel_ods import get_data
import json

#for making plot
from matplotlib import pyplot as plt
from matplotlib import style
import numpy as np
fig = plt.figure()
style.use('seaborn-bright')


def GetTrainingData():
    FileName = "training.ods"

    #Create idx # lists
    idx = 13
    colum = []
    while len(colum) <= idx:
        colum.append([])


    for i in range(1,idx):

        #import colum from file
        partial_data = get_data(FileName, start_column=i, column_limit=1)

        #Removes unneccesary part of string from jason dump 
        colum[i] = (json.dumps(partial_data).split(",",1)[1])

        #putting all the floats in the string in a list
        colum[i] = map(float, re.findall(r'[+-]?[0-9.]+', colum[i]))
        

    return colum


#fixes the bug -1*-1. This should not be shown in plot
def FixBug(list1, list2):
    for k in range(len(list1)):
        if list1[k]<0 and list2[k]<0:
            list2[k]=2


#translaterar vikten med  65 
def FixWheight(list1, reduceNum):
    for k in range(len(list1)):
        list1[k] = list1[k]-reduceNum
    return list1

#scales data points that are soposed to be ploted
def ScaleData(dataPoints, scaling):
    i = 0
    for x in dataPoints:
        if x>=0:
            dataPoints[i] = x/float(scaling)
        i = i + 1
    return dataPoints

def SetPlotStyle():
    plt.gca().set_ylim(bottom=0)
    plt.gca().set_xlim(left=0)
    plt.grid(True)
    plt.ylim([0, 12])
    plt.legend()
    plt.xlabel('Training occation')   
    plt.ylabel('Quantity')  

trainingdata = GetTrainingData()


#changing variable name for more readable code
date = trainingdata[0] #not working because of data format
ocation = trainingdata[1]
pullUps = trainingdata[2]
pushUps = trainingdata[3]
sitUps = trainingdata[4]
runningDistance = trainingdata[5]
drops = trainingdata[6]
shoulderPress=trainingdata[7]
bicepCurls=trainingdata[8]
standingRow=trainingdata[9]
backLift=trainingdata[10]
wheight=trainingdata[11]
dumbell=trainingdata[12]



#plotting begins here 

plt.figure(1)
plt.title('Body wheight workout')
scalePullUps=1
pullUps = ScaleData(pullUps, scalePullUps)
plt.plot(ocation,pullUps, 'o',label='Pull ups')

scaleSitUps=10
sitUps = ScaleData(sitUps, scaleSitUps)
plt.plot(ocation,sitUps, 'o',label='Sit ups [x%d]' %(scaleSitUps))

scalePushUps=4
pushUps = ScaleData(pushUps, scalePushUps)
plt.plot(ocation,pushUps, 'o',label='Push Ups [x%d]' %(scalePushUps))

SetPlotStyle()


plt.figure(2)
plt.title('Running')
scaleRunningDistance=1000
runningDistance = ScaleData(runningDistance, scaleRunningDistance)
plt.plot(ocation,runningDistance, 'o',label='Run [x%dm]' %(scaleRunningDistance))

scaleDrops=1
FixBug(runningDistance, drops)
drops = [x*10000/scaleRunningDistance for x in drops]
drops = np.squeeze(drops) / runningDistance
plt.plot(ocation,drops, 'D',label='Drops/10km' )

SetPlotStyle()


plt.figure(3)
plt.title('Dumbell workout') 
scaleShoulderPress=2
shoulderPress = ScaleData(shoulderPress, scaleShoulderPress)
plt.errorbar(ocation,shoulderPress, yerr=0.5, fmt='bo')
plt.plot(ocation,shoulderPress, 'o',label='Shoulder press [x%d]' %(scaleShoulderPress))

scaleBicepCurls=2
bicepCurls = ScaleData(bicepCurls, scaleBicepCurls)
plt.plot(ocation,bicepCurls, 'o',label='Bicep curls [x%d]' %(scaleBicepCurls))

scalestandingRow=2
standingRow = ScaleData(standingRow, scalestandingRow)
plt.errorbar(ocation,standingRow, xerr=(len(ocation)/30.0), fmt='ro')
plt.plot(ocation,standingRow, 'o',label='Standing row [x%d]' %(scalestandingRow))

scaleBackLift=2
backLift = ScaleData(backLift, scaleBackLift)
plt.plot(ocation,backLift, 'ko', zorder=6,label='Back lift [x%d]' %(scaleBackLift))

SetPlotStyle()


plt.figure(4)
plt.title('Wheights')
reduceWheight= 65 #kg
wheight = FixWheight(wheight, reduceWheight)
plt.plot(ocation,wheight, 'o',label='Boddy Wheight [+%dkg]' %(reduceWheight))


reduceDumbell= 10 #kg
dumbell = FixWheight(dumbell, reduceDumbell)
plt.plot(ocation,dumbell, 'o',label='Dumbell Wheight [+%dkg]' %(reduceDumbell))

SetPlotStyle()
plt.show()