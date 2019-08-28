# Info 
"dataInspector" will take the ".npy" files created in "dataProcessors" and will optimise them for the neural network. The "cnn.py" will use the optimized data to train the CNN model which is defined in the file. The collected data is split 70/30 for training and testing, this can be changed in "dataInspector". 
Once the model is trained the "use_cnn.py" will use it to get live predictions and the results will be sent to a server via "post" request the link of which can be specified in "use_cnn.py". 

#### Note: For "dataInspector" to work correctly the collected ".npy" files have to be placed in a folder called "data", which has to be in the same directory as the file itself.  

# Sample response



    {   pair: 'bitcoin',
        pred: '1', // will be same
        acc: '0.6474235',
        lastPrice: '10185.5' 
    }
    {   pair: 'ethereum',
        pred: '0', // will go down
        acc: '0.70409596',
        lastPrice: '187.52' 
    }
    {   pair: 'ripple',
        pred: '2', // will go up
        acc: '0.5155564',
        lastPrice: '0.26961799999999997' 
    }
    {   pair: 'eos', pred: '1', acc: '0.64399046', lastPrice: '3.55' }
