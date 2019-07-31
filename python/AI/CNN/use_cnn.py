from dataProvider import DataProvider
from dataGenCV import DataGenCV
import numpy as np
import cv2
from train_cnn import MMCNN
import os
from binanceCollector import BinanceCom
import time

from urllib.parse import urlencode
from urllib.request import Request, urlopen
import requests
import json

class Predictor:
    def __init__(self):
        self.__modelsFolder = "models"
        self.dp = DataProvider()
        self.dgcv = DataGenCV(self.dp)
        self.__mmcnn= MMCNN(self.dp ,self.dgcv)
        self.__posturl = 'http://10.0.0.227:9823/io/prediction' # Set destination URL here

        
        modelFolder = list(os.listdir(self.__modelsFolder))
        modelFolder = sorted(modelFolder, key=self.model_sort_key)
        print(f"\n model weights used: {modelFolder[-1]}\n")
        
        self.model = self.__mmcnn.compile_Model(self.__mmcnn.make_CNN(), weights=self.__modelsFolder+"/"+modelFolder[-1])
        
        # data = list(np.load(self.dgcv.outFile, allow_pickle=True))
        # print(self.dgcv.prepare_img_for_cnn(data[0][0], reshape=False))
        self.bc = BinanceCom()
        self.client = self.bc.connectToAccount("api_key","api_secret")
        self.pairs = self.bc.getDefaultPairs()
        self.onePair = ["XRPUSDT"]
        

    def get_prediction_from_image(self, img):
        pred = self.model.predict(img)[0]
        pred = np.array(pred)
        return np.argmax(pred), max(pred)
    
    def create_img_from_data(self, data):
        img = self.dgcv.get_img(data[0], data[1], data[2], data[3], data[4], data[5])
        img = self.dgcv.prepare_img_for_cnn(img, reshapeFour=False)
        return img
    
    def get_coin_data_from_binance(self, data, pair):
        for item in data:
            if len(item) == 60:
                item.pop(0)
                # print(len(item), "$"+str(item[-1]))
        lp, pc, high, low, _,bp, _,ap = self.bc.getData(self.client, pair)
        data[0].append(lp) 
        data[1].append(pc)
        data[2].append(high)
        data[3].append(low)
        data[4].append(bp)
        data[5].append(ap)
        return data
        
    def get_prediction_from_coin_data(self, coin_data):
        img = self.create_img_from_data(coin_data)
        pred, acc = self.get_prediction_from_image(img)
        return pred, acc
    
    def get_live_predictions(self, data_coins, pairs, callback):
        for index in range(len(pairs)):
            data_coins[index] = self.get_coin_data_from_binance(data_coins[index], pairs[index])
            pred, acc = self.get_prediction_from_coin_data(data_coins[index])
            callback(pairs[index], pred, acc, data_coins[index][0][-1])
            # print(pairs[index], "up/down: "+str(pred), str(acc)+"%", "$"+str(data_coins[index][-1]))
        return data_coins
        
    def display_predictions(self, pair, pred, acc, lastPrice):
        print(f"{pair} | Prediction: {pred} | Certainty: %{float(acc):.3f} | Price: ${float(lastPrice):.3f} ")
            
    def model_sort_key(self, item):
        return int(item.split("_")[0])
    
    def post_to_server(self, pair, pred, acc, lastPrice):
        try:
            payload = { "pair": str(pair),
                        "pred": str(pred),
                        "acc": str(acc),
                        "lastPrice": str(lastPrice)}
                        
            response_decoded_json = requests.post(self.__posturl, json=payload)
            response_json = response_decoded_json.json()

            print (response_json)
        except:
            print("Probably an issue with server, make sure server is running and 'ip' address is correct")
                
if __name__ == "__main__":
    p = Predictor()
    # pairs = p.onePair
    pairs = p.pairs
            # lp, pc, high, low, bp, ap
    data_tamplate = [[],[],[],[],[],[]]
    
    data_coins = [data_tamplate]*len(pairs)

    while True:
        # 3rd argument is a callback that takes 4 arguments (pair, prediction, accuracy, last Price)
        data_coins =  p.get_live_predictions(data_coins, pairs, p.post_to_server)
        time.sleep(60)
            