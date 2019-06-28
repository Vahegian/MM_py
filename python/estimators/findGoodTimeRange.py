import sys
import json
from datetime import date, timedelta
import matplotlib.pyplot as plt
import random

plt.switch_backend("TKAgg")
# plt.use("GTKAgg",warn=False, force=True)

def cTTGT(time):
    return int(time)/1000

def printIntDateAsNormal(id, intDate):
    try:
        print(id, date.fromtimestamp(cTTGT(intDate)))
    except:
        pass 
    
def getClosedData(jsonData, indexDataLast, indexDateBeforeIt):
    dt = list(coin_data['Close'].keys())
    lastDateAsInt = dt[indexDataLast]
    monthsBeforeAsint = dt[indexDateBeforeIt]
    printIntDateAsNormal(indexDataLast, lastDateAsInt)
    printIntDateAsNormal(indexDataLast, monthsBeforeAsint)

    dataInRange = []
    startCollecting = False
    for date in dt:
        if date == monthsBeforeAsint:
            startCollecting = True
        if startCollecting:
            dataInRange.append(coin_data['Close'][date])
        if date == lastDateAsInt:
            break
    return dataInRange

fileName = sys.argv[1] 

with open(fileName, 'r') as file:
    coin_data = json.load(file)
    
lastDate = len(coin_data['Close'])-1
twoMonths = lastDate-(2*31)

lowHighRanges = [31, 62, 93, 124] #months

rangeValueMap = {}


# will populate rangeValueMap with differences between max and min per month 
# range, find best range by finding range with consistent high/big max min gaps 
for timeRange in lowHighRanges:
    rangeReturns = []
    for date in range(-lastDate, 0):
        date = date*-1
        if date - timeRange >= 0:
            coinPriceAtDate = getClosedData(coin_data, date, date-timeRange)
            rangeReturns.append(max(coinPriceAtDate)-min(coinPriceAtDate))
        
    rangeValueMap.update({timeRange: rangeReturns})

print(rangeValueMap, rangeValueMap.keys(), len(rangeValueMap[31]))



with open("python/logs/FGTRout.txt", 'w') as logFile:
    print("LOW to HIGH Changes: " , fileName)
    logFile.write("LOW to HIGH Changes: " + fileName)
    for timeRange in list(rangeValueMap.keys()):
        output = "\ndays:"+str(timeRange)+ " max:"+ str(max(rangeValueMap[timeRange]))+\
        " mean:"+ str((sum(rangeValueMap[timeRange])/len(rangeValueMap[timeRange])))
        print(output)
        logFile.write(output)
    logFile.close()



allData = getClosedData(coin_data, lastDate, 0)

plt.plot(allData)
plt.ylabel('$ Price')
plt.show()

          




