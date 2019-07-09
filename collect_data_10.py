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
    
    def connect (self, router_name,username,password):                     #COnnect to the device and return the child process created
        child = pexpect.spawn ("telnet 10.64.97.193 2029")
        #print("telnetting")
        child.expect('\r\n')
        child.sendline('\r\n')
        
        en=child.expect(['Router>','Router#'])
        if (not en):
            child.sendline('en')
        print("Connected")
        return child 
        #
        #
    
    
    def start_cpu_data_collection (self, child,param):  #Starts data collection from child process and store it in mongo db
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
    def parse_and_get_data(self,ch,param):
        
        ch.sendline("show plat health summary all")
        time.sleep(50)
        
        try:
            ch.expect(pexpect.EOF)
        except:
           ch=str(ch.before)
           
        
        
        ch= ch.replace('\\r\\n','\n')
        rem=['\\t','|\\r\\n|','>','<','..','|','==','__','**','##','--']
        for i in rem:
            ch=ch.replace(i,'')

        f=open('parsed.txt','w')
        f.write(ch)
        f.close()
        if param=='cpu':
            cpu=re.findall(r'CPU-util\(5 min\)\s*:([^\s]+)',ch)
            print(cpu)
            val=int(cpu[0])
        elif param=='iosd':
            iosd=re.findall(r'IOSd-util\(5 min\)\s*:([^\s]+)',ch)
            val=int(iosd[0])
        elif param=='mem':
            mem=re.findall(r'Percent Used\s*:([^\s]+)',ch)
            val=int(mem[0])
        elif param=='ipv4':
            ipv4=re.findall(r'Total V4 prefixes\s*:[0-9]*/[0-9]*-([^%]+)',ch)
            val=ipv4[0]
        elif param=='ipv4':
            ipv6=re.findall(r'Total V6 prefixes\s*:[0-9]*/[0-9]*-([^%]+)',ch)
            val=ipv6[0]
        elif param=='mac':
            mac=re.findall(r'Total MACs Learnt\s*:[0-9]*/[0-9]*-([^%]+)',ch)
            val=mac[0]
        elif param=='fan':
            fan=re.findall(r'Fan-speed\s*:([^%]+)',ch)
            val=fan[0]
        elif param=='power':
            power=re.findall(r'Power consumed\s*:([^\s]+)',ch)
            val=int(power[0])                      #in watts
        elif param=='mpls':
            val=re.findall(r'Total MPLS Labels\s*:([^\s]+)',ch)
            if (not val):
                val=0 
        elif param=='tcam':
            tcam=re.findall(r'[a-z0-9A-Z\s]*\s*:[0-9]*/[0-9]*:([^%]+)',ch)
            val=sum(map(float,tcam))
        elif param=='res':
            res=re.findall(r'ID Allocation Mgr in ASICH(.*?)(?=FRU_CC)',ch,re.DOTALL)[0]
            res=re.findall(r'[a-z0-9A-Z\s]*\s*:([^%]+)',res)
            val=sum(map(float,res))
        elif param=='err':
            val=int(re.findall(r'Pending Objects\s*:([^\s]+)',ch)[0])+int(re.findall(r'Error objects\s*:([^\s]+)',ch)[0])
        elif param=='faults':
            faults=re.findall(r'Faults on the IM cardsH(.*?)(?=SERDES Fualts b/w interconnectsH)',ch,re.DOTALL)[0]
            faults=np.array(re.findall(r'[0-9]*/[0-9]*',faults))
            val=len(np.unique(faults))
        
        now = datetime.datetime.now().replace(second=0, microsecond=0) - datetime.timedelta(minutes=1) #time stamp of detected cpu usage
        next_minute = now + datetime.timedelta(minutes=1)
        
        cpu_dict = {}
        cpu_list = []
        cpu_dict["_id"] = now
        cpu_dict[param] = val
        cpu_list.append(cpu_dict.copy())
        return val
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
        
    def train_lstm_model(self, model, training_data, epochs, batch_size, lag,param,__id):
        m_train = training_data.shape[0]
        
        training_processed = training_data.loc[:__id, param].values
        np.append(training_processed,training_data.loc[__id+1:, "pred_"+param].values)
        
        training_processed = training_processed.reshape(-1,1)
        print("training",training_processed)
 
        #scaler = MinMaxScaler(feature_range = (0, 1))
        training_scaled = training_processed

        features_set = []  
        labels = []  
        for i in range(lag, m_train):  
            features_set.append(training_scaled[i-lag:i, 0])
            labels.append(training_scaled[i, 0])

        features_set, labels = np.array(features_set), np.array(labels) 
        features_set = np.reshape(features_set, (features_set.shape[0], features_set.shape[1], 1)) 

        model.fit(features_set, labels, epochs = epochs, batch_size = batch_size) 
        return model
            
    
def collect_and_store(router_name,username,password, model, __id,param):
    mydb=db()
    test_cpu=cpu()
    my_router=router()
    child = my_router.connect(router_name,username,password)
    database_name = router_name.replace(".","_")
    collection_name = param
    mongo_client=mydb.connect_to_mongo()
    
    now = datetime.datetime.now().replace(second=0, microsecond=0) - datetime.timedelta(minutes=1)
    next_date=now + datetime.timedelta(minutes=1)
    database = mongo_client[database_name]
    collection = database[collection_name]
    cur_cpu = my_router.start_cpu_data_collection(child,param)
    
    m_train = collection.find().count()
    print("m_train",m_train,"lag",lag)
    if(m_train <= lag):
        __id+=1
        collection.insert_many([{"_id": __id, "date":now, "pred_"+param:0, param:cur_cpu}])
        print("inserted",__id)
        
    else:
        __id+=1
        if(__id==6):
            mydb.insert_into_collection(mongo_client, database_name, collection_name, [{'id':__id,'date':next_date,param:cur_cpu}])
            print("inserted",__id)
        else:
            collection.update({"_id":__id},{"$set":{param:cur_cpu}})
        
        for pred_id in range(__id+1,__id+11):
            cursor = collection.find({"_id":{"$gt":__id-60}})   
            
            cpu_training_complete_temp=list(cursor)
            cpu_training_complete=pd.DataFrame(cpu_training_complete_temp)
            print(cpu_training_complete)
            print(__id)
            model = test_cpu.train_lstm_model(model, cpu_training_complete, 10, 10, lag,param,__id)
           
            predict_processed = cpu_training_complete.loc[:__id, param].values
            np.append(predict_processed,cpu_training_complete.loc[__id+1:, "pred_"+param].values)
        
            predict_processed = predict_processed.reshape(-1,1)
            test_features = []  
            for i in range(len(predict_processed)-lag, len(predict_processed)):
                test_features.append(predict_processed[i])
                    
            #scaler = MinMaxScaler(feature_range = (0, 1))
            #test_features = scaler.fit_transform(test_features)  
            test_features = np.array(test_features)  
            test_features = np.reshape(test_features, (1, lag, 1)) 
            print(test_features.shape)
            print(test_features)
                
            predictions = model.predict(test_features)
            #predictions = scaler.inverse_transform(predictions)
            predictions = float(predictions[0,0])
            print(predictions)
            print(router_name)
            
            next_date=next_date + datetime.timedelta(minutes=1)
            mydb.insert_into_collection(mongo_client, database_name, collection_name, [{"_id": pred_id, "date":next_date, "pred_"+param:predictions, param:0}])
            
        return model, __id
    
    return model, __id
    

def main():
    lag=5
    router_name=""
    
    router_name = sys.argv[1]
    username=sys.argv[2]
    password=sys.argv[3]
    param=sys.argv[4]
    features=['cpu','iosd','mem','ipv4','ipv6','mac','fan','power','mpls','tcam','res','err','faults']
    
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

    __id=-1
    while(1):
        model, __id = collect_and_store(router_name,username,password,model, __id,param)
        time.sleep(60)


    
if __name__== "__main__":
    main()
