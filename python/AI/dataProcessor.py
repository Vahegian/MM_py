import csv

# reading a csv file of coinData into list of list
class DataProcessor:
    def __init__(self):
        self.__coinData = []
        
    def get_file_content(self, link_to_file):
        with open(link_to_file, "r") as dataFile:
            content = csv.reader(dataFile, delimiter=',')
            first = True
            for row in content:
                if first:
                    first = False
                    continue
                floatRow = []
                for i in row:
                    floatRow.append(float(i))
                self.__coinData.append(floatRow)
        return self.__coinData
                
    def get_batched_data(self, link_to_file, qty=60):
        coinData = self.get_file_content(link_to_file)        
        data_batches = []
        qty = int(len(coinData)/qty+0.5)

        for num in range(qty):
            data_batches.append(coinData[num:num+60])
        return data_batches