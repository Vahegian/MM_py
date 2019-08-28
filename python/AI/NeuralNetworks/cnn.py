import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten, MaxPooling2D, Dropout
from keras.callbacks import TensorBoard, ModelCheckpoint
from keras.optimizers import SGD
from dataInspector import Inspector
import os
from datetime import date
import time


class MMCNN:
   def __init__(self):
        self.__EPOCHS = 1000
        self.f_d_layer_size = 64
        self.s_d_layer_size = 0
        self.__filepath = "models/saved-model-{epoch:02d}-{val_acc:.2f}-"+str(self.f_d_layer_size)+"-"+str(self.s_d_layer_size)+".hdf5"

   def make_CNN(self):
      # create model
        model = Sequential()
        # add model layers
        model.add(Conv2D(16, kernel_size=(5, 5), activation='relu',
                input_shape=(50, 50, 1), padding='same'))
        model.add(MaxPooling2D())
        model.add(Conv2D(32, kernel_size=(5, 5),
                activation='relu', padding='same'))
        model.add(MaxPooling2D())
        # model.add(Conv2D(64, kernel_size=(5, 5),
        #         activation='relu', padding='same'))
        # model.add(MaxPooling2D())
        model.add(Dropout(0.7))
        model.add(Flatten())
        model.add(Dense(self.f_d_layer_size, activation='relu'))
        # model.add(Dense(self.s_d_layer_size, activation='relu'))
        model.add(Dense(3, activation='softmax'))
        return model

   def compile_Model(self, model, weights=None):
        opt = SGD(lr=1e-2, momentum=0.9, decay=1e-2/self.__EPOCHS)
        if weights != None:
            print(f"\n LOADING '{weights}' \n")
            model.load_weights(weights)
        model.compile(optimizer=opt, loss='categorical_crossentropy',
                    metrics=['accuracy'])
        print(model.summary())

        return model

   def compile(self, model):
        modelFolder = list(os.listdir("models"))
        if len(modelFolder) > 0:
            modelFolder = sorted(modelFolder, key=self.model_sort_key)
            model = self.compile_Model(model, weights="models/"+modelFolder[-1])
        else:
            model = self.compile_Model(model)
        return model

   def train_model(self, model, train_x, train_y, test_x, test_y, iterations=100):
        tensorboard = TensorBoard(log_dir='./logs', histogram_freq=0,
                          write_graph=True, write_images=False)

        # checkpoint = ModelCheckpoint("./models/run1.hdf5", monitor='acc', verbose=1, save_best_only=True, mode='max')
        checkpoint = ModelCheckpoint(self.__filepath, monitor='val_acc', verbose=1, save_best_only=False, mode='max')

        model = self.compile(model)

    #   for _ in range(iterations):
        history = model.fit(train_x,train_y,epochs=self.__EPOCHS,verbose=1,validation_data=(test_x,test_y), callbacks=[tensorboard, checkpoint])
        model.save_weights(f"./models/{date.today()}_weights.h5")
        print("********************************  Saved  ************************************")
        # model_number+=1
        return history
            
   def model_sort_key(self, item):
        return int(item.split("-")[2])

   def get_prediction_from_image(self, model, img):
        pred = model.predict(img)
        pred = np.array(pred)
        return np.argmax(pred), max(pred)
     
     
if __name__ == "__main__":
    cnn = MMCNN()
    inspector = Inspector()
    training, testing = inspector.split_data(inspector.get_optimized_data())
    if int(input("To train enter '1', other number for testing\n"))==1:
        x_train, y_train, x_test, y_test = inspector.get_data_for_network(inspector.balance_Data(training))
        print(len(x_train), len(y_train), len(x_test), len(y_test))
        model = cnn.make_CNN()
        cnn.train_model(model,x_train,y_train,x_test,y_test)
    else:
        x_train, y_train, x_test, y_test = inspector.get_data_for_network(inspector.balance_Data(testing))
        # x_train = np.concatenate(x_train, x_test)
        # y_train = np.concatenate(y_train, y_test)
        print(len(x_train), len(y_train))
        model = cnn.make_CNN()
        model = cnn.compile(model)
        acc = 0.0
        loss = 0.0
        count = 0.0
        for i in range(len(x_train)):
            index, pred = cnn.get_prediction_from_image(model,np.array([x_train[i]]))
            real_val = np.argmax(y_train[i])
            same = False
            if index==real_val:
                acc+=1.0
                same = True
            else:
                loss+=1.0
            count+=1.0
            print(f"cnn: {index}\tcertainty: {max(pred):.2f}\treal: {real_val}\tloss: {float(loss/count):.2f}\tacc: {float(acc/count):.2f}\t{str(same)}")
        #     time.sleep(0.05)
            
            
        
        
    
