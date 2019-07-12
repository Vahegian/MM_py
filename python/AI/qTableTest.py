import numpy as np
from env import TradeENV
import random

tenv = TradeENV()
prices = np.load("private/crypto_with_QTBL/XRPUSDT_prices.npy")
prices = prices.tolist()
# print(prices[0])
qtables = np.load("private/crypto_with_QTBL/XRPUSDT_QTBLs.npy")

for i in range(len(qtables)-1):
    tenv.resetENV()
    qtable = qtables[i]
    priceD = prices[i]
    tenv.set_data(priceD)

    state, _, done, _ = tenv.make_step(random.randint(0,2))

    while not done:
        state, _, done, success =tenv.make_step(np.argmax(qtable[state]))
        # if success:
        tenv.showEnvState()
    