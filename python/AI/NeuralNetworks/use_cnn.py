from dataInspector import Inspector
from cnn import MMCNN
import sys
sys.path.append("../")
from dataProcessors.dataMaker import DataMaker
from collectors.fetcher import CMCFetcher

from datetime import date, timedelta
import cv2 
import numpy as np
import requests
import json
import time


def get_date_as_string(mydate):
    days = str(mydate).split("-")
    the_date = ""
    for w in days:
        the_date+=w
    return the_date
    
def post_to_server(posturl,  predictions, hists, coins):
    for i in range(len(predictions)):
        try:
            payload = { "pair": str(coins[i]),
                        "pred": str(predictions[i][0]),
                        "acc": str(predictions[i][1]),
                        "lastPrice": str(hists[i]["Close"][hists[i].index[-1]])}
                        
            response_decoded_json = requests.post(posturl, json=payload)
            response_json = response_decoded_json.json()

            print (response_json)
        except:
            print("Probably an issue with server, make sure server is running and 'ip' address is correct")
        time.sleep(0.1)
                            
def get_hist_all_coins(cf, coins, start, end):
    hists = []
    for coin in coins:
        hists.append(cf.fetch_history(coin, start=start, end=end))
    return hists

def prepare_data_for_cnn(dm, hists):
    imgs = []
    for hist in hists:
        img = dm.get_img(hist)
        # cv2.imshow("win", cv2.resize(img,(500,500)))
        # cv2.waitKey(0)
        img = inspector.optimize_img(img)
        img = np.reshape(img, (50,50,1))
        imgs.append(np.array([img]))
    return imgs

def updatePredictions(cnn, model, imgs):
    preds = []
    for img in imgs:
        index, pred = cnn.get_prediction_from_image(model,img)
        preds.append([index, max(pred)])
        print(f"cnn: {index}\tcertainty: {max(pred):.2f}\t")
    return preds 

if __name__ == "__main__":
    dm = DataMaker()
    cf = CMCFetcher()
    inspector = Inspector()
    cnn = MMCNN()
    
    model = cnn.make_CNN()
    model = cnn.compile(model)
    
    coins = ['bitcoin', 'ethereum', 'ripple', 'eos']
    
    today = date.today() 
    last_21_Days = today - timedelta(days=21)
    today = get_date_as_string(today)
    last_21_Days = get_date_as_string(last_21_Days) 
    
    hists = get_hist_all_coins(cf, coins, last_21_Days, today)
    
    imgs = prepare_data_for_cnn(dm, hists)
    
    predictions = updatePredictions(cnn, model, imgs)
    
    url = 'http://10.0.0.7:9823/io/prediction'
    post_to_server(url, predictions, hists, coins)