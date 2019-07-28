import cv2
import os
import matplotlib.pyplot as plt
plt.switch_backend("TKAgg")
import numpy as np

class DataGenCV:
    def __init__(self, dataProcessor):
        self.dp = dataProcessor
        self.folder_for_clean_data = "clean"
        self.doMin = True
        self.outFile = "charts_labels.npy"
    
    def get_percent_diff(self,curNum, nextNum):
        curNum = float(curNum)
        nextNum = float(nextNum)
        return (nextNum-curNum)/((curNum+nextNum)/2)
    
    def get_perCents(self, percent_change):
        percents = [0]*21
        if percent_change>=0.01 and percent_change<=0.25: # between 0.01 and 0.25 aka 1% and 25%
            id = round(((percent_change - 0.01) * (20 - 11) / (0.25 - 0.01) + 11))
            percents[id] = 1
            return percents
        elif percent_change>=-0.25 and percent_change<=-0.01: # between -0.01 and -0.25
            id = round(((percent_change - (-0.25)) * (9 - 0) / ((-0.01) - (-0.25)) + 0)) 
            percents[id] = 1
            return percents
        elif percent_change>-0.01 and percent_change<0.01: # between -0.01 and 0.01
            percents[10] = 1
            return percents 
        elif percent_change> 0.25:
            percents[-1] = 1
            return percents
        elif percent_change < -0.25:
            percents[0] = 1
            return percents
    
    def get_data_sets(self, data, doMIN = False):
        limit = 60
        sets = []
        subset = []
        for row in range(len(data)):
            if row % limit != 0:
                subset.append(data[row])
            else:
                try:
                    temp_list = []
                    for sec_row in range(row, row+limit):
                        temp_list.append(data[sec_row][1])
                    percent_diff = self.get_percent_diff(subset[-1][1], max(temp_list))
                    percent_diff_list = self.get_perCents(percent_diff)
                    # print(percent_diff_list)
                    sets.append([subset, percent_diff_list])
                   
                    if doMIN:
                        percent_diff = self.get_percent_diff(subset[-1][1], min(temp_list))
                        percent_diff_list = self.get_perCents(percent_diff)
                        # print(percent_diff_list)
                        sets.append([subset, percent_diff_list])
                    
                    subset = []
                except Exception:
                    print(Exception)
        return sets
                                       
    def get_transformed_img(self, convas):
        # Crop image
        img = np.array(convas)
        img = img[70:412, 105:555] # y, x         
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (60, 60))
        return img
            
    def get_charts(self, sets):
        charts_labels = []
        for subset in sets:
            lp = []
            pc = [] 
            high =[] 
            low =[] 
            bq =[] 
            bp =[] 
            aq =[]
            ap = []
            for row in subset[0]:
                # print(row)
                lp.append(row[1])
                pc.append(row[2])
                high.append(row[3])
                low.append(row[4])
                bq.append(row[5])
                bp.append(row[6])
                aq.append(row[7])
                ap.append(row[8])
                
            fig = plt.figure()    
            plt.plot(lp)#(lats price)
            plt.plot(pc)#(close_price)
            plt.plot(high)#(high)
            plt.plot(low)#(low)
            plt.plot(bp)#(bid price)
            plt.plot(ap)#(ask price)
            # plt.plot([(float(a)-float(b)) for a, b in zip(bp, bq)])#(low_data)
            # plt.plot([(float(a)-float(b)) for a, b in zip(ap, aq)])
            plt.axis('off')
            
            fig.canvas.draw()
            convas = fig.canvas.renderer.buffer_rgba()
            img = self.get_transformed_img(convas)
            charts_labels.append([img, subset[1]])
            plt.clf()
            plt.close(fig)
        return charts_labels
        
    def convertData_for_cnn(self, data):
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
        
        train_x, test_x = self.split_data(x)
        train_y, test_y = self.split_data(y)
        
        return train_x, train_y, test_x, test_y
    
    def split_data(self, data):
        data_70_percent = round(((len(data)*70)/100)+0.5)
        training = data[:data_70_percent]
        testing = data[data_70_percent:]
        return training, testing
    
    def produce_train_data(self):
        files = os.listdir(self.folder_for_clean_data)
        all_charts_and_labels = []
        for fileName in files:
            clean_file = self.folder_for_clean_data+"/"+fileName
            data = self.dp.get_file_content(clean_file, getFirst=True)
            sets = self.get_data_sets(data, doMIN=self.doMin)
            charts_labels = self.get_charts(sets)
            all_charts_and_labels = all_charts_and_labels+charts_labels
            print(len(charts_labels))
            # break
        print("all Data length: ", len(all_charts_and_labels))
        np.save(self.outFile, np.array(all_charts_and_labels))
        
        return self.convertData_for_cnn(all_charts_and_labels)
        
        
            
            
if __name__ == "__main__":
    from dataProcessor import DataProcessor
    dp = DataProcessor()
    dgcv = DataGenCV(dp)
    train_x, train_y, test_x, test_y = dgcv.produce_train_data()
    # data = list(np.load(dgcv.outFile, allow_pickle=True))
    # train_x, train_y, test_x, test_y = dgcv.convertData_for_cnn(data)
    print(len(train_x), len(train_y), len(test_x), len(test_y))        
            
                
    