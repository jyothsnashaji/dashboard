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
    mycol = mydb["cpu"]
    for i in  mycol.find({},{'_id':0,param:1}):
       li.append(i[param])
    return li

def get_network_col():
    return 'Network Health'

def get_hardware_col():
    return 'Hardware Health'

def get_software_col():
    return 'Software Health'




def get_router_id(row):
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    c=0
    for i in mongo_client.list_database_names():
       
       if row == c:
           
           return i
           break
       c=c+1