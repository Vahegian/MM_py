import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend("TKAgg")
import cv2
# import threading

class DataMaker:
    def __init__(self):
        self.__batch_size = 5
        # self.__print_lock = threading.Lock()
    def get_img_and_price_direction(self, link_to_file, outFile):
        content = np.load(link_to_file, allow_pickle=True)
        batch = int(len(content)/self.__batch_size)
        # print(content[10:20], len(content), batch)
        for i in range(batch):
            lower_limit = i*self.__batch_size
            upper_limit = lower_limit+self.__batch_size
            print(lower_limit, ":", upper_limit)
            img_price_change = self.get_3_week_plots_and_coming_price_change(content[lower_limit:upper_limit])
            self.save_created_data(img_price_change, f"{i}_{outFile}")
        # return img_price_change
    
    # def safe_print(self, message):
    #     with self.__print_lock:
    #         print(message)
    
    def save_created_data(self, content, file_name):
        # img_price_change = self.get_3_week_plots_and_coming_price_change(content)
        np.save(file_name, content)
        print(f"'{file_name}' is saved!")
    
    def get_3_week_plots_and_coming_price_change(self, content):
        img_price_changes = []
        for coin_hist in content:
            print(f"Preparing '{coin_hist[0]}' data please wait ....")
            imgs_change = self.get_plots_of_days_data_and_change(coin_hist[1])
            img_price_changes.append(imgs_change)
        return np.array(img_price_changes)   
            
    def get_plots_of_days_data_and_change(self, coin_hist, days=21):
        img_price_change=[]
        for index in range(len(coin_hist)):
            # print(coin_hist[index:index+7])
            img = self.get_img(coin_hist[index:index+days])
            change = self.get_price_change(coin_hist[index:index+days+1])
            img_price_change.append([img, change])
            # cv2.imshow("win", img)
            # print(change)
            # cv2.waitKey(10)
        return img_price_change
            
            # self.get_img(coin_hist)
            
    def get_img(self, dataframe):
        fig = plt.figure()    
        plt.plot(dataframe)
        plt.axis('off')
        
        fig.canvas.draw()
        convas = fig.canvas.renderer.buffer_rgba()
        img = self.get_transformed_img(convas)
        # plt.show()
        plt.clf()
        plt.close(fig)
        return img
    
    def get_transformed_img(self, convas):
        # Crop image
        img = np.array(convas)
        img = img[70:412, 105:555] # y, x         
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (50, 50))
        # cv2.imshow("win", img)
        # cv2.waitKey(10)
        return img
    
    def get_price_change(self, coin_hist):
        # print(coin_hist)
        mean = coin_hist[:-1]
        # print(mean)
        mean = mean["Close"].mean()
        lastPrice = coin_hist["Close"][coin_hist.index[-1]]
        # print(lastPrice)
        change = self.get_percent_diff(mean, lastPrice)
        return self.get_perCents_3_options(change)
        
    def get_percent_diff(self,curNum, nextNum):
        curNum = float(curNum)
        nextNum = float(nextNum)
        return (nextNum-curNum)/((curNum+nextNum)/2)
    
    def get_perCents_3_options(self, percent_change, action_percent=0.05):
        percents = [0]*3
        if percent_change>=action_percent:
            percents[2] = 1
            return percents
        elif percent_change<=-1*action_percent: 
            percents[0] = 1
            return percents
        elif percent_change>-1*action_percent and percent_change<action_percent:
            percents[1] = 1
            return percents 
    
    
    
if __name__ == "__main__":
    # data 
    # print(data, len(data))
    data = str(input("Please specify coin history file '.npy': \n"))
    outFile = str(input("Please specify file '.npy' to store created plots and price changes: \n"))
    if len(data)>0:
        dm = DataMaker()
        img_and_direction = dm.get_img_and_price_direction(data, outFile) # returns numpy array containing images and drice directions eg. [1,0,0]-down, [0,1,0]-no change, [0,0,1]-up
        # np.save("1.npy", img_and_direction)
        # print(img_and_direction)