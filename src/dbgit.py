from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from bson import ObjectId, json_util
import sys

DATABASE = 'CRUD-POC'

class Database():
    def __init__(self):
        try:
            #Connecting
            self.client = MongoClient('mongodb+srv://<user>:<pass>@cluster0.9s.mongodb.net/?retryWrites=true&w=majority')
            
            self.client.server_info()
            self.cnx = self.client[DATABASE]
            current_collections = self.cnx.list_collection_names()
            for collection_name in ['users']:
                if(not(collection_name in current_collections)):
                    self.cnx.create_collection(collection_name, autoIndexId=True, capped=False)
            return
        
        except ConnectionFailure as error:
            print("Connection failure")
            print(error)
            sys.exit(-1)

        except OperationFailure as error:
            print("Operation Failure")
            print(error)
            sys.exit(-2)
