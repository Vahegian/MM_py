from coinmarketcap import Market
from dataCollector import CCMCollector

class CMCFetcher:
    def __init__(self):
        self.coinmarketcap = Market()
        self.ccmc = CCMCollector()
        self.__web_link_name = "website_slug"
    
    def fetch_tickers(self, begin=0, top=100):
        tickers_data = self.coinmarketcap.ticker(start=begin, limit=top, convert='USD')["data"]
        tickers = []
        for id in tickers_data:
            tickers.append(tickers_data[id][self.__web_link_name])
            
        return tickers
    
    def fetch_history(self, ticker):
        sample_link = f"https://coinmarketcap.com/currencies/{ticker}/historical-data/?start=20140101&end=20190816"
        hist_dataFrame = self.ccmc.get_market_data(sample_link)
        return hist_dataFrame
    
    
if __name__ == "__main__":
    cmcf = CMCFetcher()
    tickers = cmcf.fetch_tickers()
    print(tickers)
    # cmcf.fetch_history(tickers[26])