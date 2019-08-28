
class TradeENV:
    def __init__(self):
        self.resetENV()
        self.__coinData = None
        self.__ACTION_REWARD = 10
        self.__PROFIT_REWARD = 100
        self.__LOSS_PENALTY = -100
        self.__REWARD = 50
        self.__PENALTY = -50
        self.__NO_REWARD = 0
        self.__dataLength = 0
        self.target = 1000
        self.fee = 0.1
        self.min_allowed_trade_amount = 10

        
    def set_data(self, data):
        # print(data)
        self.__coinData = data
        self.__dataLength = len(data)

    def make_step(self, step):
        if self.__coinData == None:
            return
        reward = 0
        # tempWallet = self.__wallet_available
        done = False
        target_reached = False
        
        if step == 0:
            bought = self.__buy(self.__coin_Data_Cur_Id)
            if bought:
                reward = self.__getBuyReward(self.__coin_Data_Cur_Id)
            else:
                reward = self.__PENALTY
        elif step == 1:
            sold = self.__sell(self.__coin_Data_Cur_Id)
            if sold:
                reward = self.__getSellReward(self.__coin_Data_Cur_Id)
            else:
                reward = self.__PENALTY
        elif step == 2:
            curAmount = self.__coinData[self.__coin_Data_Cur_Id][1]*self.__coin_qyt
            if curAmount > self.__wallet_before_buy:
                reward = self.__PROFIT_REWARD
            elif curAmount < self.__wallet_before_buy:
                reward = self.__PENALTY
            else:
                reward = self.__ACTION_REWARD
                
        if self.__wallet_available >= self.target or self.__coin_Data_Cur_Id>= len(self.__coinData)-1:
            done = True
        else:
            done = False
        
        if self.__wallet_available >= self.target:
            target_reached = True
        
        self.__coin_Data_Cur_Id+=1
        
        newState = self.__getNewState(self.__coin_Data_Cur_Id)
        
        return (newState ,reward, done, target_reached)
        
    def __sell(self, priceId):
        price = self.__coinData[priceId][1]
        if self.__coin_qyt*price < self.min_allowed_trade_amount:
            return False
        self.__wallet_available = (self.__coin_qyt*price) - ((self.fee/100.0)*(self.__coin_qyt*price))
        self.__coin_qyt = 0
        return True
    
    def __getSellReward(self, priceId):
        soldPrice = self.__coinData[priceId][1]
        if soldPrice > self.__curBuyPrice and self.__wallet_available > self.__wallet_before_buy:
            return self.__PROFIT_REWARD
        elif soldPrice == self.__curBuyPrice:
            return self.__PENALTY
        else:
            return self.__LOSS_PENALTY
                   
    def __buy(self, priceId):
        if self.__wallet_available < self.min_allowed_trade_amount:
            return False
        price = self.__coinData[priceId][1] #1 gets lastPrice, 2 will get prevClosedPrice
        availableAfterFee = self.__wallet_available - ((self.fee/100.0)*self.__wallet_available)
        self.__coin_qyt =  availableAfterFee / price
        self.__wallet_before_buy = self.__wallet_available
        self.__wallet_available = 0.0 
        self.__curBuyPrice = price
        return True
    
    def __getBuyReward(self, priceID):  
        buyPrice = self.__coinData[priceID][1]
        best_price_after = min([i[1] for i in self.__coinData[priceID:priceID+30]])
        if buyPrice < best_price_after:
            return self.__ACTION_REWARD+self.__REWARD+self.__PROFIT_REWARD
        elif buyPrice == best_price_after:
            return self.__ACTION_REWARD+self.__REWARD
        else:
            return self.__LOSS_PENALTY
        
    def __getNewState(self, priceId):
        dataSlice = self.__coinData[priceId-5:priceId-1]
        prices = [i[1] for i in dataSlice]
        min_of_range = min(prices)
        max_of_range = max(prices)
        x_pos = min(self.__coinData[priceId-4][1], self.__coinData[priceId-5][1])
        y_pos = min(self.__coinData[priceId-2][1], self.__coinData[priceId-3][1])
        
        # print(x_pos, min_of_range, max_of_range, 0.0, self.dataLength)
        # print(y_pos, min_of_range, max_of_range, 0, self.dataLength)

        x_pos = self.__map_values(x_pos, min_of_range, max_of_range, 0.0, self.__dataLength-1)
        y_pos = self.__map_values(y_pos, min_of_range, max_of_range, 0.0, self.__dataLength-1)
        return (int(x_pos+0.5), int(y_pos+0.5))
        
    def __map_values(self, x, in_min, in_max, out_min, out_max): 
        return ((x - in_min) * (out_max - out_min)) / ((in_max - in_min) + out_min)
                
    def showEnvState(self):
        print(f"wallet: {self.__wallet_available}, coin qyt: {self.__coin_qyt}")
        
    def get_Env_dimantions(self):
        return (self.__dataLength, self.__dataLength)
    def reset_id(self):
        self.__coin_Data_Cur_Id = 4
    
    def resetENV(self):
        self.__wallet_available = 100
        self.__wallet_before_buy = 0.0
        self.__coin_qyt = 0
        self.__coin_Data_Cur_Id = 4
        self.__curBuyPrice = 0.0
    
if __name__ == "__main__":
    
    from dataProcessor import DataProcessor
    import random

    dp = DataProcessor()
    data_batches = dp.get_batched_data("private/cryptoMinute/XRPUSDT.csv") # add data clean method to class
    # print(data_batches, len(data_batches))
        
    # using the env.
    te = TradeENV()      
    # te.set_data(data_batches[10])

    for data in data_batches:
        te.set_data(data)
        te.reset_id()
        for rounds in range(len(data)-4):
            step = te.make_step(random.randint(0,2))    
            te.showEnvState()
        
        
    
# step = te.make_step(0)
# print(step)
# te.showEnvState()

# step = te.make_step(2)
# print(step)
# te.showEnvState()

# step = te.make_step(1)
# print(step)
# te.showEnvState()