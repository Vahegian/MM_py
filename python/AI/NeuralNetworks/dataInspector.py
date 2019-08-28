import numpy as np
import cv2
import os

class Inspector:
    def __init__(self):
        pass
    
    def get_optimized_data(self):
        files = os.listdir('./data')
        # print(files, len(files))
        all_content = []
        for data_file in list(files):
            try:
                if int(data_file[0])>-1:
                    print(f"working on '{data_file}'...")
                    content = np.load("./data/"+data_file, allow_pickle=True)
                    for item in list(content):
                        for img_d in item[:-22]: # remove last 22 items because they might be corrupt
                            # img_d[0] = cv2.cvtColor(img_d[0], cv2.COLOR_BGR2GRAY)
                            # img_d[0] = img_d[0]/255.0
                            img_d[0]=self.optimize_img(img_d[0])
                            img_d[1] = np.array(img_d[1])
                            all_content.append(img_d)
            except:
                print(f"'{data_file}' is not a data file!")
        print(f"Total number of data points = {len(all_content)}")
        return all_content  
    
    def optimize_img(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = img/255.0
        return img
    
    def balance_Data(self, data):
      data_to_balance = [[],[],[]]
      for item in data:
         if item[1][0] == 1:
            data_to_balance[0].append(item)
         elif item[1][1]== 1:
            data_to_balance[1].append(item)
         elif item[1][2] == 1:
            data_to_balance[2].append(item)
      print("down: ", len(data_to_balance[0]), "same: ", len(data_to_balance[1]), "up: ", len(data_to_balance[2]))
      min_amount = 1000000000
      for data in data_to_balance:
         data_len = len(data)
         if data_len < min_amount:
            min_amount = data_len
      balanced_data = []
      for index in range(min_amount):
         for data in data_to_balance:
            balanced_data.append(data[index])
      print("balanced Data length: ", len(balanced_data))
      return np.array(balanced_data)  
  
    def split_data(self, data, percent=70):
        data_percent = round(((len(data)*percent)/100)+0.5)
        training = data[:data_percent]
        testing = data[data_percent:]
        return training, testing
    
    def get_data_for_network(self, data):
        train, test = self.split_data(data, percent=80)
        x_train = []
        y_train = []
        x_test = []
        y_test = []
        for train_item in train:
            x_train.append(np.reshape(train_item[0], (50,50,1)))
            y_train.append(train_item[1])
            
        for test_item in test:
            x_test.append(np.reshape(test_item[0], (50,50,1)))
            y_test.append(test_item[1]) 
        return np.array(x_train),np.array(y_train) ,np.array(x_test) ,np.array(y_test) 
                


if __name__ == "__main__":
    i = Inspector()
    training, testing = i.split_data(i.get_optimized_data()) 
    x_train, y_train, x_test, y_test = i.get_data_for_network(i.balance_Data(training))
    print(len(x_train), len(y_train), len(x_test), len(y_test))
    