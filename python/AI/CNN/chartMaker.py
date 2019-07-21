# from dataProcessor import DataProcessor
import os
import matplotlib.pyplot as plt
plt.switch_backend("TKAgg")

class ChartMaker:
    def __init__(self, dataProcessor):
        self.dp = dataProcessor
        self.futurePrices = 60 # minutes in future
        self.futureMax = True
        self.train_folder = "train_data"
        
    def get_percent_diff(self,curNum, nextNum):
        return (nextNum-curNum)/((curNum+nextNum)/2)
    
    def get_next_10_max(self, id, data):
        nums = []
        try:
            for i in range(1, self.futurePrices):
                nums.append(data[id+i][1])
            # print("after for")
            if self.futureMax:
                return max(nums)
            else:
                return min(nums)
        except Exception:
            print(Exception)
            return False
        
    def set_future_minutes(self, minutes):
        self.futurePrices = minutes 
    
    def set_future_max(self, true_false):
        self.futureMax = true_false 
                
    def __get_data_sets(self, data):
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
                nextMax = self.get_next_10_max(id, data)
                if not nextMax:
                    break
                perDiff = self.get_percent_diff(data[id][1], nextMax)
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
        return sets    
        
    def creat_folder(self, path_to_folder):
        try:
            os.makedirs(path_to_folder)
        except FileExistsError:
            # directory already exists
            print("Exists: ", path_to_folder)
            
    def make_charts_from_data(self, link_to_clean_data_folder):
        self.creat_folder(self.train_folder)
        files = os.listdir(link_to_clean_data_folder)
        for fileName in files:
            clean_file = link_to_clean_data_folder+"/"+fileName
            data = self.dp.get_file_content(clean_file)
            
            sets = self.__get_data_sets(data)

            # print(sets,len(sets))
            imID = 0
            prices = ""
            
            if self.futureMax:
                feature_folder = self.train_folder+"/"+str(self.futurePrices)+"_max"
            else:
                feature_folder = self.train_folder+"/"+str(self.futurePrices)+"_min"
            self.creat_folder(feature_folder)
            
            coin = fileName.split('.')[0][:-4]
            coin_folder = feature_folder+"/"+coin[6:]
            self.creat_folder(coin_folder)
            
            img_folder = coin_folder+"/IMG"
            self.creat_folder(img_folder)
            
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
                plt.savefig(img_folder+"/"+str(imID)+".png")
                plt.clf()
                imID+=1          
                
            with open(coin_folder+"/prices.csv", "w") as outFile:
                outFile.write(prices)    
            

    # plt.show()