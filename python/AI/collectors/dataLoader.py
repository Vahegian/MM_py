import numpy as np
from cleaner import DataCleaner

def save_data_in_npy(file_name, data_in_numpy):
    np.save(file_name, data_in_numpy)   
    print(f"{file_name} saved!") 

if __name__ == "__main__":
    out_file = input("Please specify a '.npy' file to store data to \n")
    if len(out_file)>0:
        data_cleaner = DataCleaner()

        data_in_numpy = data_cleaner.get_cleaned_data()
        print(data_in_numpy, len(data_in_numpy))
        save_data_in_npy(out_file, data_in_numpy)
    else:
        print("Bad Output file!")
    


    # train_data, test_data = split_data(data_in_numpy, split=70)

    # train_x, train_y, test_x, test_y = get_training_data(train_data)
