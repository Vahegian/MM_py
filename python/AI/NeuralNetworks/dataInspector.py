import numpy as np
import cv2
import os

if __name__ == "__main__":
    # content = np.load(, allow_pickle=True)
    # print(content[0][0][0], len(content))
    # outFile = input("please specify 'output.npy' file: \n")
    files = os.listdir('./')
    # print(files, len(files))
    count = 0
    all_content = []
    for data_file in list(files):
        try:
            if int(data_file[0])>-1:
                print(f"working on '{data_file}'...")
                content = np.load(data_file, allow_pickle=True)
                for item in list(content):
                    for img_d in item[:-22]: # remove last 22 items because they might be corrupt
                        # img = cv2.resize(img_d[0], (500, 500))
                        # img_d = [img_d[0]/255.0, img_d[1]]
                        img_d[0] = cv2.cvtColor(img_d[0], cv2.COLOR_BGR2GRAY)
                        img_d[0] = img_d[0]/255.0
                        img_d[1] = np.array(img_d[1])
                        all_content.append(img_d)
                        count+=1
                        # print(img_d[1], count)
                        # cv2.imshow("win", img)
                        # cv2.waitKey(100)
        except:
            print(f"'{data_file}' is not a data file!")
    print(f"Total number of data points = {len(all_content)}", count)
    # new_data = np.array(all_content)
    # np.save(outFile, new_data)
    # print(f"{outFile} saved!", new_data)                
    