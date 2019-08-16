## Information about the scripts

* The "dataLoader.py" is the main script, the other files contain classes to help it collect "coin" history from "coinmarketcap" website 
* The collected data can be stored in ".npy" file, which has to be specified after running the script.
* The ".npy" file can later be used for manipulating the collected data with other scripts. 

### Note: One file "dataCollector.py" is missing for privacy reasons the file must use api keys to fetch historical data from an exchange or other service. The file has to contain a method named "get_market_data(url)" which takes an "url" and returns a "pandas" dataframe.   
