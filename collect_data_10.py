    #Application to accept router name as input and continously collect data and make predictions

#inputs
lag=10
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
    
    def connect (self, router_name,username,password):         #COnnect to the device and return the childprocess created
        child = pexpect.spawn ("telnet 10.64.97.193 2029")
        #print("telnetting")
        child.expect('\r\n')
        child.sendline('\r\n')
        
        en=child.expect(['Router>','Router#'])
        if (not en):
            child.sendline('en')
        print("Connected")
        return child 
        
    def parse_and_get_data(self,ch):
        ch.sendline("show plat health summary all")
        time.sleep(50)
        
        try:
            ch.expect(pexpect.EOF)
        except:
            pass
            
        child=ch
        ch=str(ch.before)
           
        
        
        ch= ch.replace('\\r\\n','\n')
        rem=['\\t','|\\r\\n|','>','<','..','|','==','__','**','##','--']
        for i in rem:
            ch=ch.replace(i,'')

        f=open('parsed.txt','w')
        f.write(ch)
        f.close()
    
        cpu=re.findall(r'CPU-util\(5 min\)\s*:([^\s]+)',ch)
        cpu=int(cpu[0])

        iosd=re.findall(r'IOSd-util\(5 min\)\s*:([^\s]+)',ch)
        iosd=int(iosd[0])
        

        mem=re.findall(r'Percent Used\s*:([^\s]+)',ch)
        mem=int(mem[0])
        

        ipv4=re.findall(r'Total V4 prefixes\s*:[0-9]*/[0-9]*-([^%]+)',ch)
        ipv4=ipv4[0]
        
        ipv6=re.findall(r'Total V6 prefixes\s*:[0-9]*/[0-9]*-([^%]+)',ch)
        ipv6=ipv6[0]
        
        mac=re.findall(r'Total MACs Learnt\s*:[0-9]*/[0-9]*-([^%]+)',ch)
        mac=mac[0]
        
        fan=re.findall(r'Fan-speed\s*:([^%]+)',ch)
        fan=fan[0]
        
        power=re.findall(r'Power consumed\s*:([^\s]+)',ch)
        power=int(power[0])                      #in watts
      

        mpls=re.findall(r'Total MPLS Labels\s*:([^\s]+)',ch)
        if (not mpls):
            mpls=0 
        
        tcam=re.findall(r'[a-z0-9A-Z\s]*\s*:[0-9]*/[0-9]*:([^%]+)',ch)
        tcam=sum(map(float,tcam))
        
        res=re.findall(r'ID Allocation Mgr in ASICH(.*?)(?=FRU_CC)',ch,re.DOTALL)[0]
        res=re.findall(r'[a-z0-9A-Z\s]*\s*:([^%]+)',res)
        res=sum(map(float,res))
        
        err=int(re.findall(r'Pending Objects\s*:([^\s]+)',ch)[0])+int(re.findall(r'Error objects\s*:([^\s]+)',ch)[0])
        
        faults=re.findall(r'Faults on the IM cardsH(.*?)(?=SERDES Fualts b/w interconnectsH)',ch,re.DOTALL)[0]
        faults=np.array(re.findall(r'[0-9]*/[0-9]*',faults))
        faults=len(np.unique(faults))
        

        print(cpu,iosd,mem,ipv4,ipv6,mac,fan,power,mpls,tcam,res,err,faults)
        return child,{'cpu':cpu,'iosd':iosd,'mem':mem,'ipv4':ipv4,'ipv6':ipv6,'mac':mac,'fan':fan,'power':power,'mpls':mpls,'tcam':tcam,'res':res,'err':err,'faults':faults}

   
    
    
class db:
    
    def connect_to_mongo (self):        #Connects to local mongo database
        mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        return (mongo_client)
    def insert_init(self,router_name,__id):

        database_name = router_name.replace(".","_")
        collection_name = "data"
        mongo_client=self.connect_to_mongo()
    
        now = datetime.datetime.now().replace(second=0, microsecond=0) #- datetime.timedelta(minutes=1)
        next_date=now + 10*datetime.timedelta(minutes=1)
        database = mongo_client[database_name]
        collection = database[collection_name]
        if  __id<=10:
            collection.insert_many([{"_id": __id, "date":now}])
        #features=['cpu','iosd','mem','ipv4','ipv6','mac','fan','power','mpls','tcam','res','err','faults']

        #pr={x:0 for x in features}
        collection.insert_many([{"_id": __id+11, "date":next_date}])
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
        
    def train_lstm_model(self, model, training_data, epochs, batch_size, lag,param,__id,pred_id):
        m_train = training_data.shape[0]
        training_processed = training_data.loc[:__id-1, param].values
        if pred_id!=__id:
            #print("processing",__id," ",pred_id,training_processed,training_data.loc[__id:pred_id-1,"pred_"+param].values)
            training_processed=np.concatenate((training_processed,training_data.loc[__id:pred_id-1,"pred_"+param].values),axis=0)
            #print("now",training_processed)
        training_processed = training_processed.reshape(-1,1)
        print(training_processed)
 
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
            
    
def collect_and_store(router_name, model, __id,feature,cur_):
    mydb=db()
    test_cpu=cpu()
    
    database_name = router_name.replace(".","_")
    collection_name = "data"
    mongo_client=mydb.connect_to_mongo()
    database = mongo_client[database_name]
    collection = database[collection_name]

    

    m_train = collection.find().count()-12
    if(m_train <= lag):
        collection.update({"_id":__id},{"$set":{"pred_"+feature:0, feature:cur_[feature]}})
        __id+=1
        m_train+=1
        #print(m_train-1)
    else:
        collection.update({"_id":__id},{"$set":{feature:cur_[feature]}})
        __id+=1
        print(__id-1,"updated")

    if m_train>lag:

        
        for pred_id in range(__id,__id+10):
            cursor = collection.find({"_id":{"$in":list(range(__id-60,pred_id))}})    
            cpu_training_complete_temp=list(cursor)
            cpu_training_complete=pd.DataFrame(cpu_training_complete_temp)
            
            
            
            predict_processed = cpu_training_complete.loc[:, feature].values
            predict_processed = predict_processed.reshape(-1,1)
            test_features = [] 
            future_cpu = cpu_training_complete.loc[:, "pred_"+feature].values
            future_cpu = future_cpu.reshape(-1,1) 


            for i in range(pred_id-lag, __id):
                    test_features.append(predict_processed[i])
            for i in range(__id , pred_id):
                    test_features.append(future_cpu[i])
                    
            #scaler = MinMaxScaler(feature_range = (0, 1))
            #test_features = scaler.fit_transform(test_features)  
            test_features = np.array(test_features)  
            test_features = np.reshape(test_features, (1, lag, 1)) 
            
            print(test_features)
            
            model = test_cpu.train_lstm_model(model, cpu_training_complete, 10, 10, lag,feature,__id,pred_id)    
            predictions = model.predict(test_features)
            #predictions = scaler.inverse_transform(predictions)
            predictions = float(predictions[0,0])
            print(predictions)
            
            
            collection.update({"_id":pred_id},{"$set":{"pred_"+feature:predictions}})
            

    
    return model

def main():
    lag=10
   
    
    router_name = sys.argv[1]
    username=sys.argv[2]
    password=sys.argv[3]
    features=['cpu','iosd','mem','ipv4','ipv6','mac','fan','power','mpls','tcam','res','err','faults']
    models={}
    for feature in features:
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
        models[feature]=model
    __id=0 ##########################################
    mydb=db()
    my_router=router()
    child =my_router.connect(router_name,username,password)
    while(__id>=0):
        child,cur_=my_router.parse_and_get_data(child)
        mydb.insert_init(router_name,__id)
        for feature in features:
            models[feature] = collect_and_store(router_name,models[feature],__id,feature,cur_)
        __id=__id+1
        

    
if __name__== "__main__":
    main()