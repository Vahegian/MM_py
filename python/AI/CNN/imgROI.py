import cv2
import numpy as np
import os
import csv


class DataOptimizer:
    def __init__(self):        
        self.folder = "train_data"
        self.imgFolder = "IMG"
        self.outFolder = "60x60"
        self.outFile = "img_label001.npy"
        self.labelFile = "prices.csv" 

    def creat_folder(self, path_to_folder):
        try:
            os.makedirs(path_to_folder)
        except FileExistsError:
            # directory already exists
            print("Exists: ", path_to_folder)
            
    def get_perCents(self, percent_change):
        percents = [0]*21
        if percent_change>=0.01 and percent_change<=0.25: # between 0.05 and 0.5 aka 5% and 50%
            id = round(((percent_change - 0.01) * (20 - 11) / (0.25 - 0.01) + 11))
            percents[id] = 1
            return percents
        elif percent_change>=-0.25 and percent_change<=-0.01: # between -0.05 and -0.5
            id = round(((percent_change - (-0.25)) * (9 - 0) / ((-0.01) - (-0.25)) + 0)) 
            percents[id] = 1
            return percents
        elif percent_change>-0.01 and percent_change<0.01: # between -0.05 and 0.05
            percents[10] = 1
            return percents        

        
    def transform_data(self):
        dataFolders = os.listdir(self.folder)
        for dataFolder in dataFolders:
            coinFolders = os.listdir(self.folder+"/"+dataFolder)
            for coinFolder in coinFolders:
                # num_files = os.listdir(folder+dataFolder+coinFolder+imgFolder)
                # print(len(num_files))
                writeFolder = self.folder+"/"+dataFolder+"/"+coinFolder+"/"+self.outFolder 
                self.creat_folder(writeFolder)    
                lables = []
                with open(self.folder+"/"+dataFolder+"/"+coinFolder+"/"+self.labelFile, "r") as dataFile:
                    content = csv.reader(dataFile, delimiter=',')
                    lables = list(content)[0][:-1]
                # print(lables)
                lable_id = 0
                img_and_label = []
                img_folder = os.listdir(self.folder+"/"+dataFolder+"/"+coinFolder+"/"+self.imgFolder)
                for imgName in img_folder:
                    # Read image
                    im = cv2.imread(self.folder+"/"+dataFolder+"/"+coinFolder+"/"+self.imgFolder+"/"+imgName)
                        
                    # Crop image
                    imCrop = im[70:412, 105:555] # y, x
                    
                    im = cv2.cvtColor(imCrop, cv2.COLOR_BGR2GRAY)
                    
                    im = cv2.resize(im, (60, 60))

                    img_and_label.append([im, self.get_perCents(float(lables[lable_id]))])
                    
                    
                    lable_id+=1
                    
                np.save(writeFolder+"/"+self.outFile, img_and_label)
                print("saved ..........")   
                    
                    
                    # # Display image
                    # cv2.imshow("Image", im)
                    
                    # cv2.waitKey(10)

# if __name__ == '__main__' :
    # transform_data()
    
    # print(0.1,get_perCents(0.1))
    # print(0.45,get_perCents(0.45))
    # print(0.5,get_perCents(0.5))
    # print(-0.1,get_perCents(-0.1))
    # print(-0.45,get_perCents(-0.45))
    # print(-0.5,get_perCents(-0.5))
    # print(-0.40,get_perCents(-0.40))
    # print(0, get_perCents(0))
    # data = np.load(folder+dataFolders[0]+coinFolders[4]+outFolder+"/img_label.npy", allow_pickle=True)
    # print(data)