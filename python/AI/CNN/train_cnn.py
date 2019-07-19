import numpy as np

folder = "train_data/"
dataFolders = ["60_max/","60_min/","180_max/","180_min/","360_max/","360_min/"]
coinFolders = ["BAT/","BTC/","EOS/","ETH/","XRP/"]
img_label_folder = "60x60/"
img_label_file = "img_label.npy"

def get_traning_data():
    img_label_data = []
    for dataFolder in dataFolders:
        for coinFolder in coinFolders:
            img_label_data.append(list(np.load(folder+dataFolder+coinFolder+img_label_folder+img_label_file, allow_pickle=True)))
    train_data = []
    
    for data in img_label_data:
        # print(data.shape)
        train_data = train_data+data
            
    print(len(train_data))
    data_70_percent = round(((len(train_data)*70)/100)+0.5)
    training = train_data[:data_70_percent]
    testing = train_data[data_70_percent:]
    return training, testing
    

if __name__ == "__main__":
    training, testing = get_traning_data()
    print(len(training), len(testing))
    
    