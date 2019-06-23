import sys
import json
from datetime import date, timedelta

with open(sys.argv[1], 'r') as file:
    coin_data = json.load(file)

dt = list(coin_data['Open'].keys())[2]

print(type(dt), dt)
dt = date.fromtimestamp(int(dt)/1000)
print(dt)
print(dt- timedelta(days=32))

# for timedate in coin_data['Open'].keys(): 
#     datetime = date.fromtimestamp(int(timedate)/1000)
#     print(datatime)
    # datetime

# def findPrevYare(diff, upperYare):
#     var = diff - () 

