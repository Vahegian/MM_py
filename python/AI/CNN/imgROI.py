import cv2
import numpy as np
import os
import csv

folder = "train_data/"
dataFolders = ["60_max/","60_min/","180_max/","180_min/","360_max/","360_min/"]
coinFolders = ["BAT/","BTC/","EOS/","ETH/","XRP/"]
imgFolder = "IMG/"
extention = ".png"
outFolder = "60x60"
labelFile = "prices.csv" 

def creat_folder(path_to_folder):
    try:
        os.makedirs(path_to_folder)
    except FileExistsError:
        # directory already exists
        print("Exists: ", path_to_folder)
        
def transform_data():
    for dataFolder in dataFolders:
        for coinFolder in coinFolders:
            num_files = os.listdir(folder+dataFolder+coinFolder+imgFolder)
            print(len(num_files))
            writeFolder = folder+dataFolder+coinFolder+outFolder 
            creat_folder(writeFolder)    
            lables = []
            with open(folder+dataFolder+coinFolder+labelFile, "r") as dataFile:
                content = csv.reader(dataFile, delimiter=',')
                lables = list(content)[0][:-1]
            # print(lables)
            lable_id = 0
            img_and_label = []
            for imgName in range(len(num_files)):
                # Read image
                im = cv2.imread(folder+dataFolder+coinFolder+imgFolder+str(imgName)+extention)
                    
                # Crop image
                imCrop = im[70:412, 105:555] # y, x
                
                im = cv2.cvtColor(imCrop, cv2.COLOR_BGR2GRAY)
                
                im = cv2.resize(im, (60, 60))
                
                img_and_label.append([im, lables[lable_id]])
                
                
                lable_id+=1
                
            np.save(writeFolder+"/img_label.npy", img_and_label)
            print("saved ..........")   
                
                
                # # Display image
                # cv2.imshow("Image", im)
                
                # cv2.waitKey(10)

if __name__ == '__main__' :
    transform_data()
    # data = np.load(folder+dataFolders[0]+coinFolders[4]+outFolder+"/img_label.npy", allow_pickle=True)
    # print(data)