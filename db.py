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

def get_title(param):
    titles={'cpu':'Total CPU Utilization','iosd':'IOSd Process Utilization','mem':'Total Memory Utilization',
    'ipv4':'IPv4 Route Utilization','ipv6':'IPv6 Route Utilization','mac':'MAC Table Utilization',
    'fan':'Fan Speed','power':'Power','mpls':'MPLS Label Utilization','tcam':'External TCAM(KBP) Utilization',
    'res':'ID Allocation','err':'Errors/Pending Objects','faults':'Faults on the IM cards'}
    return titles[param]


def get_col(param,router_id):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    
    #now = datetime.datetime.now().replace(second=0, microsecond=0) -2* datetime.timedelta(minutes=1) #time stamp of detected cpu usage

    
    mydb = myclient[router_id]
    mycol = mydb["data"] 
    li=[]    
    for i in  mycol.find({param:{"$exists":True}},{'_id':0,param:1}):
       li.append(i[param])
    return [l for l in li if l!='ff']          
                     
    

#print(get_col("_id","10_64_97_193"))




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
  
    return df



def compute_score(router_id,param):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[router_id]
    mycol = mydb["data"] 
    
    now = datetime.datetime.now().replace(second=0, microsecond=0) -3* datetime.timedelta(minutes=1) #time stamp of detected cpu usage
   


    if (param=="summary"):
        return max(compute_score(router_id,"network"),compute_score(router_id,"hardware"),compute_score(router_id,"software"))
    pr={x:1 for x in get_col_group(param)}
    
    df=list(mycol.find({"_id":1},projection={**pr,**{"_id":0}})) #fix now
    print(df)
    
    if param=="hardware":
        act=float(df[0]["power"])
        df[0].update({"power":act/12})                  ####change here to get power from console
    if any(float(x)>95 for x in list(df[0].values())):
        score=150
    elif any(float(x)>85 for x in list(df[0].values())):
        score=90
    else:
        score=30
    return score
   
#print(compute_score("1_1_1_1","summary"))
