import pandas as pd
import pymongo
import numpy as np
import pandas as pd
import time
import pexpect
import re
import datetime

def get_list_of_routers():
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    l=[]
    for i in mongo_client.list_database_names():
        if i in ['admin','config','local']:
            continue
        else:
            l.append(i)
    
    return l


def get_col(param,router_id):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    li=[]
    
    mydb = myclient[router_id]
    mycol = mydb["cpu"]                     #######################change here!
    for i in  mycol.find({},{'_id':0,param:1}):
       li.append(i[param])
    return li






def get_router_id(row):
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    c=0
    for i in mongo_client.list_database_names():
       
       if row == c:
           
           return i
       c=c+1
def get_col_group(param):
    
    if param=="network":
        df=["ipv4","ipv6","mpls","mac"]
    elif param=="software":
        df=["iosd","res","err"]
    elif param=="hardware":
        df=["cpu","mem","fan","power","tcam","faults"]
    else:
        pass
    return df


def compute_score(router_id,param):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[router_id]
    mycol = mydb["data"] 
    
    now = datetime.datetime.now().replace(second=0, microsecond=0) - datetime.timedelta(minutes=1) #time stamp of detected cpu usage
    
    #df=list(mycol.find({"_id":0},{x:1 for x in get_col_group(param)})))
    df=[{'_id': 0, 'ipv4': '0.01', 'ipv6': '0.01', 'mac': '0.0', 'mpls': 0}]
    
    if any(float(x)>95 for x in list(df[0].values())):
        score=150
    elif any(float(x)>85 for x in list(df[0].values())):
        score=90
    else:
        score=30
    return score

compute_score("1_1_1_1","network")
    