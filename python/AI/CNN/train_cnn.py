import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D
from keras.callbacks import TensorBoard, ModelCheckpoint
from dataProvider import DataProvider
from dataGenCV import DataGenCV

class MMCNN:
   def __init__(self, dp, dgcv):
      self.dp = dp
      self.dgcv = dgcv

   def make_CNN(self):
      #create model
      model = Sequential()
      #add model layers
      model.add(Conv2D(32, kernel_size=(5,5), activation='relu', input_shape=(60,60,1), padding='same'))
      model.add(MaxPooling2D())
      model.add(Conv2D(64, kernel_size=(5,5), activation='relu', padding='same')) 
      model.add(MaxPooling2D())
      model.add(Flatten())
      model.add(Dense(1024, activation='relu'))
      model.add(Dense(21, activation='softmax'))      
      
      return model
   
   def compile_Model(self, model, weights=None):
      if weights !=None:
         model.load_weights(weights)
      model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
      print(model.summary())
   
      return model
   
   def get_training_data(self):
      # if data is not processed and saved in '.npy'
      train_x, train_y, test_x, test_y = self.dp.clean_data_cv_only()
      print(len(train_x), len(train_y), len(test_x), len(test_y))
      return train_x,train_y,test_x,test_y 

   def get_training_data_from_file(self):
      data = list(np.load(self.dgcv.outFile, allow_pickle=True))
      train_x, train_y, test_x, test_y = self.dgcv.convertData_for_cnn(data)
      print(len(train_x), len(train_y), len(test_x), len(test_y))
      return train_x,train_y,test_x,test_y
   
   def train_model(self, model, train_x,train_y,test_x,test_y, iterations=100, EPOCHS=10):
      tensorboard = TensorBoard(log_dir='./logs', histogram_freq=0,
                          write_graph=True, write_images=False)
      
      #checkpoint = ModelCheckpoint("./models/run1.hdf5", monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    
      for i in range(iterations):
         history = model.fit(train_x,train_y,epochs=EPOCHS,verbose=1,validation_data=(test_x,test_y), callbacks=[tensorboard])
         model.save_weights(f"./models/{i}_weights.h5")
         print("********************************  Saved  ************************************")
      return history
            

    

if __name__ == "__main__":
   dp = DataProvider()
   dgcv = DataGenCV(dp)
   mmcnn = MMCNN(dp, dgcv)
    
   train_x, train_y, test_x, test_y = mmcnn.get_training_data()
   # train_x, train_y, test_x, test_y = mmcnn.get_training_data_from_file()
   
   model = mmcnn.make_CNN()
   
   model = mmcnn.compile_Model(model)
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
      
     
    
    
    
