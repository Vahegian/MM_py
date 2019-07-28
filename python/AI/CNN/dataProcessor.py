import csv

# reading a csv file of coinData into list of list
class DataProcessor:
    def __init__(self):
        pass
        
    def get_file_content(self, link_to_file, getFirst=False):
        coinData = []
        with open(link_to_file, "r") as dataFile:
            content = csv.reader(dataFile, delimiter=',')
            first = getFirst
            for row in content:
                if not first:
                    first = True
                    continue
                floatRow = []
                for i in row:
                    floatRow.append(float(i))
                coinData.append(floatRow)
        return coinData
                
    def get_batched_data(self, link_to_file, qty=60):
        coinData = self.get_file_content(link_to_file)        
        data_batches = []
        qty = int(len(coinData)/qty+0.5)

        for num in range(qty):
            data_batches.append(coinData[num:num+60])
        return data_batches
    
    def clean_fix_content(self, link_to_file, keep_first_line=True, write_to_file=False):
        coinData = self.get_file_content(link_to_file)
        print(len(coinData))
        newData = []
        tempData = []
        if keep_first_line:
            newData.append(coinData[0])
        minute = 1
        for num in range(0, len(coinData)):
            # print(int(coinData[num][0]), minute)
            if int(coinData[num][0]) == minute:
                 tempData.append(coinData[num])
                 if minute != 60:
                    minute+=1
                 else:
                    minute=1
                    newData+=tempData
                    tempData =[]
            elif int(coinData[num][0]) == 1:
                tempData = []
                tempData.append(coinData[num])
                minute = 2
        if write_to_file:
            newFile = link_to_file.split('.')
            newlink = newFile[0]+"_Clean."+newFile[1]
            self.write_data_to_file(newlink, newData)
        return newData
    
    def write_data_to_file(self, link_to_file, data):
        with open(link_to_file, "w") as outFile:
            writer = csv.writer(outFile)
            writer.writerows(data)
        
                

# if __name__ == "__main__":
    # dp = DataProcessor()
    # flink = "private/cryptoMinute/XRPUSDT.csv"
    # cdata = dp.clean_fix_content(flink, keep_first_line=False, write_to_file=True)   