from dataProcessor import DataProcessor
import matplotlib.pyplot as plt
plt.switch_backend("TKAgg")

coins = ["BAT","BTC","EOS","ETH","XRP"]

for coin in coins:
    clean_file = "cleans/"+coin+"USDT_Clean.csv"
    futurPrices = 6*60 # minutes in future


    dp = DataProcessor()
    data = dp.get_file_content(clean_file)

    def get_percent_diff(curNum, nextNum):
        return (nextNum-curNum)/((curNum+nextNum)/2)

    def get_next_10_max(id):
        nums = []
        try:
            for i in range(1, futurPrices):
                nums.append(data[id+i][1])
            return min(nums)
        except:
            return False

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
            nextMax = get_next_10_max(id)
            if not nextMax:
                break
            perDiff = get_percent_diff(data[id][1], nextMax)
            print(data[id][1], nextMax, perDiff)
            subset.append(perDiff) #percent diff after 10 min
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
        plt.savefig("train_data/"+coin+"/IMG/"+str(imID)+".png")
        plt.clf()
        imID+=1          
        
    with open("train_data/"+coin+"/prices.csv", "w") as outFile:
        outFile.write(prices)    
            

    # plt.show()