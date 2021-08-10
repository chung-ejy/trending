from pymongo import MongoClient, DESCENDING
import pandas as pd
from datetime import timedelta
from database.idatabase import IDatabase

## https://realpython.com/python-super/
class ADatabase(IDatabase):

    def __init__(self,database_name):
        self.database_name = database_name
        super().__init__()
    
    def connect(self):
        self.client = MongoClient("localhost",27017)

    def close(self):
        self.client.close()

    def store_data(self,table_name,ds):
        try:
            db = self.client[self.database_name]
            table = db[table_name]
            records = ds.to_dict("records")
            table.insert_many(records)
        except Exception as e:
            print(self.database_name,table_name,str(e))
    
    def retrieve_data(self,table_name):
        try:
            db = self.client[self.database_name]
            table = db[table_name]
            data = table.find(show_record_id=False)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.database_name,table_name,str(e))
            return None
            
    def retrieve_query(self,table,query):
        try:
            db = self.client[self.database_name]
            table = db[table]
            data = table.find(query,show_record_id=False)
            return pd.DataFrame(list(data))
        except Exception as e:
            print(self.database_name, table,str(e))
            return None

    def drop_table(self,table_name):
        try:
            db = self.client[self.database_name]
            table = db[table_name]
            table.drop()
        except Exception as e:
            print(self.database_name,table_name,str(e))
            return None
    
    def set_index(self,table_name,index_col):
        try:
            db = self.client[self.database_name]
            table = db[table_name]
            table.create_index([(index_col,-1)])
        except Exception as e:
            print(self.database_name,table_name,str(e))
            return None   

    def reset(self):
        try:
            self.db.connect()
            db = self.client[self.database_name]
            collections = db.list_collection_names()
            for collection in collections:
                table = db[collection]
                table.drop()
            self.db.close()
        except Exception as e:
            print(self.database_name,str(e))
            return None  