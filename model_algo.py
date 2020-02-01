import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import  LSTM,Dense

def model_lstm(value):
    global actual,pred_date
    
# load the data
    path="Data\\year\\"
    df = pd.read_csv(path+f"{value}.csv")

    

# data extraction for forcasting
    
    new_data = pd.DataFrame(index=range(0,len(df)),columns=['TIMESTAMP', 'CLOSE'])
    
    new_data['TIMESTAMP'] = df['TIMESTAMP'].values
    new_data['CLOSE'] = df['CLOSE'].values
    
    
    new_data.index = new_data.TIMESTAMP
    new_data.drop('TIMESTAMP', axis=1, inplace=True)
    dataset = new_data.values
    
# fix Train And Test data set size    
    train,valid = new_data[0:int(len(df)*0.8)],new_data[int(len(df)*0.8):]
    
# Scaling the data 
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)
    

# creating traing data     
    x_train, y_train = [], []
    for i in range(50,len(train)):
        x_train.append(scaled_data[i-50:i,0])
        y_train.append(scaled_data[i,0])
        
# convert the training data in array         
    x_train, y_train = np.array(x_train), np.array(y_train)
    
    
# reshape the data    
    x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))
    
# create and fit the LSTM network
    model = Sequential()
    model.add(LSTM(units=40, return_sequences=True, input_shape=(x_train.shape[1],1)))
    model.add(LSTM(units=40))
    model.add(Dense(1))
    
#compiling loss
    model.compile(loss='mean_squared_error', optimizer='sgd')
    model.fit(x_train, y_train, epochs=10, batch_size=32, verbose=1)
    
#predicting values, using past 50 days  data from the train data
    inputs = new_data[len(new_data) - len(valid) - 50:].values
    inputs = inputs.reshape(-1,1)
    inputs  = scaler.transform(inputs)

#creating test data
    X_test = []
    for i in range(50,inputs.shape[0]):
        X_test.append(inputs[i-50:i,0])
    X_test = np.array(X_test)
    
    X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
    
#Apply the algo (prediction)
    closing_price = model.predict(X_test)
    
# invert transformation (convert scaled data to normal or original data )
    closing_price = scaler.inverse_transform(closing_price)
    
# calculating Root Mean Square (rms)
    rms=np.sqrt(np.mean(np.power((valid-closing_price),2)))
    rms
    
    
    pd.set_option('mode.chained_assignment', None)
    
# creating result sets
    valid['Predictions'] = closing_price
    actual=pd.DataFrame(train['CLOSE'])
    pred_date=pd.DataFrame(valid['Predictions'])
    
    
    
   

