import db
import numpy as np
import pymongo

def get_list_of_routers():
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
    l=[]
    for i in mongo_client.list_database_names():
        if i in ['admin','config','local']:
            continue
        else:
            l.append(i)
    l=[i.replace('_','.') for i in l ]
    return l
print(get_list_of_routers())
