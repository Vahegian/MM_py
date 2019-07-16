from dataProcessor import DataProcessor
import matplotlib.pyplot as plt
plt.switch_backend("TKAgg")

dp = DataProcessor()
data = dp.get_file_content("python/AI/CNN/train_data/ETHUSDT_Clean.csv")

minutes = []
open_data = []
high_data = []
low_data = []
close_data = []
sets = []
limit = 60
subset = []
id = 0
for row in data:
    # print(int(row[0]), limit)
    if int(row[0]) != limit:
        minutes.append(row[0])
        open_data.append(row[1])
        close_data.append(row[2])
        high_data.append(row[3])
        low_data.append(row[4])
    else:
        subset.append(open_data)
        subset.append(close_data)
        subset.append(high_data)
        subset.append(low_data)
        subset.append(data[id][1]) #price after 1 hour
        sets.append(subset)
        subset = []
        minutes = []
        open_data=[]
        close_data=[]
        high_data=[]
        low_data=[]
    id+=1

# print(sets,len(sets))
imID = 0
prices = ""
for data in sets:
    # print(data[4])
    # break
    plt.plot(data[0])#(open_data)
    plt.plot(data[1])#(close_data)
    plt.plot(data[2])#(high_data)
    plt.plot(data[3])#(low_data)
    prices+=str(data[4])+"," # price after 1 hour
    plt.axis('off')
    # plt.show()
    # break
    plt.savefig("python/AI/CNN/train_data/ETH/IMG/"+str(imID)+".png")
    plt.clf()
    imID+=1          
    
with open("python/AI/CNN/train_data/ETH/prices.csv", "w") as outFile:
    outFile.write(prices)    
          

# plt.show()