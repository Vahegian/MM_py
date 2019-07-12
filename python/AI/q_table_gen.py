import numpy as np
from env import TradeENV
from dataProcessor import DataProcessor
import random
import os

class GEN_Q_TABLE:
    def __init__(self, link_To_Data):        
        self.__LEARNING_RATE = 0.1
        self.__DISCOUNT = 0.95
        self.__EPISODES = 15000
        self.__SHOW_EVERY = 3000

        self.__tEnv = TradeENV()
        dp = DataProcessor()
        self.__data_batches = dp.get_batched_data(link_To_Data) 

        # Exploration settings
        self.__epsilon = 1  # not a constant, qoing to be decayed
        self.__START_EPSILON_DECAYING = 1
        self.__END_EPSILON_DECAYING = self.__EPISODES//2
        self.__epsilon_decay_value = self.__epsilon/(self.__END_EPSILON_DECAYING - self.__START_EPSILON_DECAYING)
        
    def __getFileData(self, file_to_save_to):
        if os.path.isfile(file_to_save_to):
            print('File exists, loading previous data!')
            return list(np.load(file_to_save_to))
        else:
            print('File doesn\'t exist: Creating a file ... ')
            return []

    def createTables(self, qtbl_file_to_save_to, prices_file_to_save_to):
        qtbl_data_to_save = self.__getFileData(qtbl_file_to_save_to)
        prices_data_to_save = self.__getFileData(prices_file_to_save_to)
        
        id = 1
        for data in self.__data_batches:
            self.__tEnv.resetENV()
            print("data: ", id)
            self.__tEnv.set_data(data)
            Q_TABLE_X_DEPT , Q_TABLE_Y_DEPT = self.__tEnv.get_Env_dimantions()
            Q_TABLE_OPTIONS_DEPT = 3
            q_table = np.random.uniform(low=-2, high=0, size=(Q_TABLE_X_DEPT,Q_TABLE_Y_DEPT,Q_TABLE_OPTIONS_DEPT))
            id+=1
            for episode in range(self.__EPISODES):
                self.__tEnv.reset_id()
                discrete_state, _, _, _ = self.__tEnv.make_step(random.randint(0,2))  #[10,19] = [-0.xx, -0.ttt, 0]
                done = False
                    
                while not done:

                    if np.random.random() > self.__epsilon:
                        # Get action from Q table
                        action = np.argmax(q_table[discrete_state])
                    else:
                        # Get random action
                        action = np.random.randint(0, 2)

                    # print(action)
                    new_discrete_state, reward, done, target_reached = self.__tEnv.make_step(action)
                
                    # if reward > 0:
                    #     print(new_discrete_state, reward, done)
                    #     self.__tEnv.showEnvState()
                        
                    # If simulation did not end yet after last step - update Q table
                    if not done:

                        # Maximum possible Q value in next step (for new state)
                        max_future_q = np.max(q_table[new_discrete_state])

                        # Current Q value (for current state and performed action)
                        current_q = q_table[discrete_state + (action,)]

                        # And here's our equation for a new Q value for current state and action
                        new_q = (1 - self.__LEARNING_RATE) * current_q + self.__LEARNING_RATE * (reward + self.__DISCOUNT * max_future_q)

                        # Update Q table with new Q value
                        q_table[discrete_state + (action,)] = new_q

                    discrete_state = new_discrete_state

                # Decaying is being done every episode if episode number is within decaying range
                if self.__END_EPSILON_DECAYING >= episode >= self.__START_EPSILON_DECAYING:
                    self.__epsilon -= self.__epsilon_decay_value
                   
                if episode % self.__SHOW_EVERY == 0:
                    self.__tEnv.showEnvState()
                    if target_reached:
                        qtbl_data_to_save.append(q_table)
                        prices_data_to_save.append(data) 
                # if target_reached:
                #     qtbl_data_to_save.append(q_table)
                #     prices_data_to_save.append(data)
                    
            np.save(qtbl_file_to_save_to, qtbl_data_to_save)
            np.save(prices_file_to_save_to, prices_data_to_save)
            print("Data saved ...")

gqt = GEN_Q_TABLE("private/cryptoMinute/XRPUSDT.csv")
gqt.createTables("private/crypto_with_QTBL/XRPUSDT_QTBLs1.npy", "private/crypto_with_QTBL/XRPUSDT_prices1.npy")

# data = np.load("private/crypto_with_QTBL/XRPUSDT_prices.npy")
# data2 = np.load("private/crypto_with_QTBL/XRPUSDT_QTBLs.npy")
# print(len(data2), len(data))