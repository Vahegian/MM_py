import csv
import numpy as np
from fetcher import CMCFetcher
import time


class DataCleaner:
    def __init__(self):
        self.data_fetcher = CMCFetcher()
        
    def get_cleaned_data(self):
        tickers = self.data_fetcher.fetch_tickers(top=100) # returns ["BTC", "ETH", .....]
        tickers_and_hist = self.get_ticker_history(tickers) # returns a np array ["btc", [hist]]
        clean_hist = self.clean_data(tickers_and_hist) # returns np array ["btc", [hist]] with clean data
        return clean_hist
        # content = self.get_file_content()
        
    def get_ticker_history(self, tickers):
        # print(tickers)
        content = []
        # count = 0
        for ticker in tickers:
            # if count==10:
            #     print("waiting for server...")
            #     time.sleep(60)
            #     count = 0
            try:
                hist = self.data_fetcher.fetch_history(ticker) # returns pandas dataframe
                time.sleep(60) # to Not stress the server
                content.append([ticker, hist])
                print(f"fetched '{ticker}' history.")
                # count+=1
            except:
                print(f"Could Not fetch '{ticker}' history!")
            
            
        return np.array(content)
    
    def clean_data(self, tickers_and_hist):
        clean_data = []
        for ticker in tickers_and_hist:
            ticker[1].dropna(inplace=True)
            clean_data.append(ticker)
        # print(clean_data, len(tickers_and_hist))
        return clean_data        
