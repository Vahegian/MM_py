import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D
from keras.callbacks import TensorBoard, ModelCheckpoint
from keras.optimizers import SGD
from dataProvider import DataProvider
from dataGenCV import DataGenCV
import os

class MMCNN:
   def __init__(self, dp, dgcv):
      self.dp = dp
      self.dgcv = dgcv
      self.__EPOCHS = 50

   def make_CNN(self):
      #create model
      model = Sequential()
      #add model layers
      model.add(Conv2D(32, kernel_size=(5,5), activation='relu', input_shape=(60,60,1), padding='same'))
      model.add(MaxPooling2D())
      model.add(Conv2D(64, kernel_size=(5,5), activation='relu', padding='same')) 
      model.add(MaxPooling2D())
      model.add(Conv2D(128, kernel_size=(5,5), activation='relu', padding='same')) 
      model.add(MaxPooling2D())
      model.add(Flatten())
      model.add(Dense(1024, activation='relu'))
      model.add(Dense(1024, activation='relu'))
      model.add(Dense(3, activation='softmax'))      
      
      return model
   
   def compile_Model(self, model, weights=None):
      opt = SGD(lr=1e-2, momentum=0.9, decay=1e-2/self.__EPOCHS)
      if weights !=None:
         print(f"\n LOADING '{weights}' \n")
         model.load_weights(weights)
      model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
      print(model.summary())
   
      return model
   
   def get_training_data(self):
      # if data is not processed and saved in '.npy'
      train_x, train_y, test_x, test_y = self.dp.clean_data_cv_only()
      print(len(train_x), len(train_y), len(test_x), len(test_y))
      return train_x,train_y,test_x,test_y 
   
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
      
         

   def get_training_data_from_file(self):
      data = list(np.load(self.dgcv.outFile, allow_pickle=True))
      data = self.balance_Data(data)
      train_x, train_y, test_x, test_y = self.dgcv.convertData_for_cnn(data)
      print(len(train_x), len(train_y), len(test_x), len(test_y))
      return train_x,train_y,test_x,test_y
   
   def train_model(self, model, train_x,train_y,test_x,test_y, iterations=100):
      tensorboard = TensorBoard(log_dir='./logs', histogram_freq=0,
                          write_graph=True, write_images=False)
      
      #checkpoint = ModelCheckpoint("./models/run1.hdf5", monitor='val_acc', verbose=1, save_best_only=True, mode='max')
      modelFolder = list(os.listdir("models"))
      model_number = 0
      
      if len(modelFolder)>0:
         modelFolder = sorted(modelFolder, key=self.model_sort_key)
         model_number = int(modelFolder[-1].split("_")[0])+1
         model = self.compile_Model(model, weights="models/"+modelFolder[-1])
      else:
         model = self.compile_Model(model)
    
      for _ in range(iterations):
         history = model.fit(train_x,train_y,epochs=self.__EPOCHS,verbose=1,validation_data=(test_x,test_y), callbacks=[tensorboard])
         model.save_weights(f"./models/{model_number}_weights.h5")
         print("********************************  Saved  ************************************")
         model_number+=1
      return history
            
   def model_sort_key(self, item):
         return int(item.split("_")[0])
    

if __name__ == "__main__":
   dp = DataProvider()
   dgcv = DataGenCV(dp)
   mmcnn = MMCNN(dp, dgcv)
   
   if int(input("Enter: \n'1'-for preparing data \n'any other number'-for training\n")) == 1:
      train_x, train_y, test_x, test_y = mmcnn.get_training_data()
   else:
      train_x, train_y, test_x, test_y = mmcnn.get_training_data_from_file()
   
      model = mmcnn.make_CNN()
   
      # model = mmcnn.compile_Model(model)
      hist = mmcnn.train_model(model,train_x, train_y, test_x, test_y) 
    
   #  '''   
   #     ***takes long to process data***
    
   #  # *** if data is not processed use this ***
   #  train_x, train_y, test_x, test_y = dp.get_dataSets()
    
   #  # *** if data is processed and u trying to retrain use this ***
   #  # train_x, train_y, test_x, test_y = dp.get_data()
    
   #  '''
    
   #  ''' *** faster version *** '''
    
   #  # if data is not processed and saved in '.npy'
   #  # train_x, train_y, test_x, test_y = dp.clean_data_cv_only()
   #  # print(len(train_x), len(train_y), len(test_x), len(test_y))        

    
   #  # if data was saved with previous step
   #  dgcv = DataGenCV(dp)
   #  data = list(np.load(dgcv.outFile, allow_pickle=True))
   #  train_x, train_y, test_x, test_y = dgcv.convertData_for_cnn(data)
   #  ''' *****************************************************   '''
    
   #  model = make_CNN()
    
   #  tensorboard = TensorBoard(log_dir='./logs', histogram_freq=0,
   #                        write_graph=True, write_images=False)
   # #  checkpoint = ModelCheckpoint("./models/run1.hdf5", monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    
   #  for i in range(100):
   #    history = model.fit(train_x,train_y,epochs=10,verbose=1,validation_data=(test_x,test_y), callbacks=[tensorboard])
   #    model.save_weights(f"./models/{i}_weights.h5")
   #    print("********************************  Saved  ************************************")
      
     
    
    
    
