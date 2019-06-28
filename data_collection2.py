    #Application to accept router name as input and continously collect data and make predictions

#inputs
lag=5
import pymongo
import numpy as np
import pandas as pd
import time
import pexpect
import re
import datetime
import random
import sys
from keras.models import Sequential  
from keras.layers import Dense  
from keras.layers import LSTM  
from keras.layers import Dropout  

from sklearn.preprocessing import MinMaxScaler 



class router:
    
    def connect (self, router_name):                     #COnnect to the device and return the child process created
        child = pexpect.spawn ("ssh <your cisco id>@vayu-auto-lnx")
        child.expect ('password:')
        child.sendline ("<Your cisco password>")
        child.expect('Kickstarted')
        #print("ssh done")
        child.sendline ("telnet "+router_name)
        child.expect('User Access Verification')
        #print("Telnet done")
        child.expect('Password:')
        #print("Telnet password")
        child.sendline("lab")
        child.expect(">")
        #print("Telnet done")
        child.sendline("en")  
        child.expect("Password: ")
        #print("Enable password request")
        child.sendline("lab")
        child.expect("#")
        #print(child.before)
        #child.sendline("terminal length 0")
        return child 
        #
        #
        #
    
    def start_cpu_data_collection (self, child):  #Starts data collection from child process and store it in mongo db
        f=open("cpu_pexpect.txt","w")
        child.sendline("sh proce cpu plat hist 1min")
        
        child.expect("1 minutes ago, CPU utilization: [0-9]+%")
        #print(child.after)
        f.write(child.after)
        f.close()
        
        #print("data collecting")
        
        now = datetime.datetime.now().replace(second=0, microsecond=0) - datetime.timedelta(minutes=1) #time stamp of detected cpu usage
        next_minute = now + datetime.timedelta(minutes=1)
        
        f=open("cpu_pexpect.txt","r")
        a=f.read()
        f.close()
        x=re.findall("[0-9]+",a)
        #print x
        #a=np.array(x)
        #cpu=a.reshape(255,2)
        #print(cpu.shape)
        #print cpu
        #df=pd.DataFrame(data=cpu[0:,1:], index=cpu[0:,0], columns=cpu[0,1:]) 
        #df.columns=["cpu"]
        #df.to_csv("cpu_pexcept_csv.csv")        
        #
        #
        cpu_dict = {}
        cpu_list = []
        cpu_dict["_id"] = now
        cpu_dict["cpu"] = x[1]
        cpu_list.append(cpu_dict.copy())
        print(cpu_list)    
        return x[1]
    
class db:
    
    def connect_to_mongo (self):        #Connects to local mongo database
        mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        return (mongo_client)
    
    def insert_into_collection (self, mongo_client, database_name, collection_name, values_dict):
        #if (not(database_name in mongo_client.list_database_names())):
            #print ("Error : Database doest not exist!")
            #return None
        database = mongo_client[database_name]
        #if (not(collection_name in database.list_collection_names())):
            #print ("Error : Collection does not exist!")
            #return None            
        collection = database[collection_name]
        x = collection.insert_many(values_dict)
        return x.inserted_ids        
    
    def empty_collection (self, mongo_client, database_name, collection_name):
        if (not(database_name in mongo_client.list_database_names())):
            print ("Error : Database doest not exist!")
            return None
        database = mongo_client[database_name]
        if (not(collection_name in database.list_collection_names())):
            print ("Error : Collection does not exist!")
            return None            
        collection = database[collection_name]
        x = collection.delete_many({})
        return x.deleted_ids
        
class cpu:
        
    def train_lstm_model(self, model, training_data, epochs, batch_size, lag):
        m_train = training_data.shape[0]
        training_processed = training_data.loc[:, "cpu"].values
        training_processed = training_processed.reshape(-1,1)
        print(training_processed)
 
        scaler = MinMaxScaler(feature_range = (0, 1))
        training_scaled = scaler.fit_transform(training_processed)  

        features_set = []  
        labels = []  
        for i in range(lag, m_train):  
            features_set.append(training_scaled[i-lag:i, 0])
            labels.append(training_scaled[i, 0])

        features_set, labels = np.array(features_set), np.array(labels) 
        features_set = np.reshape(features_set, (features_set.shape[0], features_set.shape[1], 1)) 

        model.fit(features_set, labels, epochs = epochs, batch_size = batch_size) 
        return model
            
    
def collect_and_store(router_name, model, __id):
    mydb=db()
    test_cpu=cpu()
    my_router=router()
    child = my_router.connect(router_name)
    database_name = router_name.replace(".","_")
    collection_name = "cpu"
    mongo_client=mydb.connect_to_mongo()
    
    now = datetime.datetime.now().replace(second=0, microsecond=0) - datetime.timedelta(minutes=1)
    next_date=now + datetime.timedelta(minutes=1)
    database = mongo_client[database_name]
    collection = database[collection_name]
    cur_cpu = my_router.start_cpu_data_collection(child)
    
    m_train = collection.find().count()
    if(m_train <= lag):
        collection.insert_many([{"_id": __id, "date":now, "pred_cpu":0, "cpu":cur_cpu}])
        __id+=1
        m_train+=1
        print(m_train+1)
    else:
        collection.update({"_id":__id},{"$set":{"cpu":cur_cpu}})
        __id+=1
        print(m_train)
        
    if(m_train > lag):
        cursor = collection.find({"_id":{"$gt":__id-60}})    
        cpu_training_complete_temp=list(cursor)
        cpu_training_complete=pd.DataFrame(cpu_training_complete_temp[0:m_train])
        print(cpu_training_complete)
        
        model = test_cpu.train_lstm_model(model, cpu_training_complete, 10, 10, lag)
        predict_processed = cpu_training_complete.loc[:, "cpu"].values
        predict_processed = predict_processed.reshape(-1,1)
        test_features = []  
        for i in range(m_train-lag, m_train):  
            test_features.append(predict_processed[i])
                
        scaler = MinMaxScaler(feature_range = (0, 1))
        test_features = scaler.fit_transform(test_features)  
        test_features = np.array(test_features)  
        test_features = np.reshape(test_features, (1, lag, 1)) 
        print(test_features.shape)
        print(test_features)
            
        predictions = model.predict(test_features)
        predictions = scaler.inverse_transform(predictions)
        predictions = float(predictions[0,0])
        print(predictions)
        print(router_name)
            
        mydb.insert_into_collection(mongo_client, database_name, collection_name, [{"_id": __id, "date":next_date, "pred_cpu":predictions, "cpu":0}])
            
        return model, __id
    
    return model, __id
    

def main():
    lag=5
    router_name=""
    for arg in sys.argv[1:]:
        router_name = arg

    model = Sequential()  
    model.add(LSTM(units=4, return_sequences=True, input_shape=(lag, 1))) 
    model.add(Dropout(0.2)) 

    model.add(LSTM(units=4, return_sequences=True))  
    model.add(Dropout(0.2))

    model.add(LSTM(units=4, return_sequences=True))  
    model.add(Dropout(0.2))

    model.add(LSTM(units=4))  
    model.add(Dropout(0.2)) 

    model.add(Dense(units = 1)) 

    model.compile(optimizer = 'adam', loss = 'mean_squared_error') 

    __id=0
    while(1):
        model, __id = collect_and_store(router_name, model, __id)
        time.sleep(60)


    
if __name__== "__main__":
    main()
