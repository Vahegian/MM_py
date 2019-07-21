import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D
from keras.callbacks import TensorBoard, ModelCheckpoint
from dataProvider import DataProvider

def make_CNN():
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
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    print(model.summary())
    
    return model
    

if __name__ == "__main__":
    dp = DataProvider()
    
    # *** if data is not processed use this ***
    train_x, train_y, test_x, test_y = dp.get_dataSets()
    
    # *** if data is processed and u trying to retrain use this ***
    # train_x, train_y, test_x, test_y = dp.get_data()
    
    model = make_CNN()
    
    tensorboard = TensorBoard(log_dir='./logs', histogram_freq=0,
                          write_graph=True, write_images=False)
    checkpoint = ModelCheckpoint("./models/run1.hdf5", monitor='val_acc', verbose=1, save_best_only=True, mode='max')
    
    history = model.fit(train_x,train_y,epochs=5,verbose=1,validation_data=(test_x,test_y), callbacks=[tensorboard, checkpoint])
    
    
    