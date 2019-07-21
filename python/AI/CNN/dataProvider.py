from dataProcessor import DataProcessor
import os
import csv
from chartMaker import ChartMaker
from imgROI import DataOptimizer
import numpy as np


class DataProvider:
    def __init__(self):
        self.__collected_data_folder = "private/cryptoMinute"
        self.dp = DataProcessor()
        self.folder_for_clean_data = "clean"
        self.cm = ChartMaker(self.dp)
        self.__futur_hours = 6
        self.do = DataOptimizer()
        self.__folder = "train_data"
        self.__img_label_folder = "60x60"
        self.__img_label_file = "img_label001.npy"
        
    def cleanData(self, link_to_data_folder):
        files = os.listdir(link_to_data_folder)
        # print(files)
        self.__creat_folder(self.folder_for_clean_data)
        
        for fileName in files:
            cleanData = self.dp.clean_fix_content(link_to_data_folder+"/"+fileName, keep_first_line=False, write_to_file=False)
            self.dp.write_data_to_file(self.folder_for_clean_data+"/clean_"+fileName, cleanData)
    
    def __creat_folder(self, path_to_folder):
        try:
            os.makedirs(path_to_folder)
        except FileExistsError:
            # directory already exists
            print("Exists: ", path_to_folder)
            
    def make_charts_and_future_prices(self):
        for i in range(1, self.__futur_hours+1):
            self.cm.set_future_max(True)
            self.cm.set_future_minutes(i*60)
            self.cm.make_charts_from_data("clean")
            self.cm.set_future_max(False)
            self.cm.make_charts_from_data("clean")
            
    def optimize_data_for_cnn(self):
        self.do.transform_data()
        
    def __get_traning_test_data(self):
        img_label_data = []
        dataFolders = os.listdir(self.__folder)
        for dataFolder in dataFolders:
            coinFolders = os.listdir(self.__folder+"/"+dataFolder)
            for coinFolder in coinFolders:
                img_label_data.append(list(np.load(self.__folder+"/"+dataFolder+"/"+coinFolder+"/"+self.__img_label_folder+"/"+self.__img_label_file, allow_pickle=True)))
        train_data = []
        
        for data in img_label_data:
            # print(data.shape)
            train_data = train_data+data
                
        print(len(train_data))
        data_70_percent = round(((len(train_data)*70)/100)+0.5)
        training = train_data[:data_70_percent]
        testing = train_data[data_70_percent:]
        return training, testing
    
    def __convertData_for_cnn(self, data):
        x = []
        y = []
        for array in data:
            # print(x.shape, array[0].shape)
            x.append(array[0])
            # np.append(x, array[0], axis = 0)
            y.append(array[1])
        #     print(array[1])
        
        # print(len(x), len(y))
    
        x = np.array(x)
        x = x.reshape(len(x), 60, 60, 1)
        x = x.astype('float32')
        x /=255.0
        
        y = np.array(y)
        
        return x, y
        
    
    def get_dataSets(self):
        training, testing = self.__get_traning_test_data()
        # print(len(training), len(testing))
        trainX, trainY = self.__convertData_for_cnn(training)
        testX, testY = self.__convertData_for_cnn(testing)
        
        return trainX, trainY, testX, testY 
    
    def get_data(self):
        self.cleanData(self.__collected_data_folder)
        self.make_charts_and_future_prices()
        self.optimize_data_for_cnn()
        return self.get_dataSets()

# if __name__ == "__main__":
#     dp = DataProvider()
#     # dp.cleanData("private/cryptoMinute")
#     # dp.make_charts_and_future_prices()
#     # dp.optimize_data_for_cnn()
#     a,b,s,d = dp.get_dataSets()
#     print(len(a), len(b), len(s), len(d))
    
    
                
        