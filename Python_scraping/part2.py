
'''
this is used to open all files related to one user and insert all their content into the mongodb databases amalgamated into 1 document per user including 'endo' the user's endomondo id and 'array' an array of the user's endomodo activies from jan 1 2015 to june 1 2015
'''

import os
import pymongo
from pymongo import MongoClient
import json
import pickle

client = MongoClient()
db = client.endo
collection = db.users
collection_runs = db.runs

#your file structure
home_dir = "/home/ubuntu/python/pytest2/data"
min_user_id = 20218312

#first we open we each 
list_dir = os.listdir(home_dir)
for user_dir in list_dir:    
    for user_file in os.listdir(x):
        string_to_read = "%s/%s"%(user_dir,user_file) 
        with open(string_to_read, 'r') as f:
            json_record = json.loads(f.read())
            collection.update({"endo":json_record["endo"]}, {'$set':{"endo":json_record["endo"]}, '$push':{"activityArray": {"$each":json_record["array"]}}}, upsert=True)

#for each user, look up the details of each activity listed on the general user page
#code assumes if you are adding users incrementally that you started with a low id and have
#worked your way up
master_list = list()
cursor = collection.find({"endo":{'$gte':min_user_id} ,"activityArray":{"$elemMatch":{"sport":0}}},{"activityArray.sport" : 1, "activityArray.id":1, "endo" : 1})
for result_object in cursor:
        for i in result_object["activityArray"]:
            if(i["sport"]==0):
                collection_runs.update({"run":i["id"]}, {'$set':{"endo":result_object["endo"]}}, upsert = True)
                master_list.append({"endo":result_object["endo"], "runID":i["id"]})
                print "just inserted into databases for user %s for run %s"%(result_object["endo"], i["id"])


#separately save list of all run activities as a pickled object for easy access for later use
with open('master_list_runs.pickle', 'wb') as handle:
        pickle.dump(master_list, handle)
