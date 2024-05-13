from pymongo import MongoClient
from data import Data



class Db(object):

    def __init__(self, DB_NAME):
        self.DB_NAME = DB_NAME

    def download_all(self, username):
        client = MongoClient()
        db = client[self.DB_NAME]
        table = db[username]

        images = table.find()
        
        datas = []
        for image in images:
            datas.append(Data.from_db(image))

        return datas
    
    def download(self, username, filename):
        client = MongoClient()
        db = client[self.DB_NAME]
        table = db[username]

        image = table.find_one({"filename":filename})
        return Data.from_db(image)
    
    def upload(self, username, data):
        client = MongoClient()
        db = client[self.DB_NAME]
        table = db[username]

        data_id = table.insert_one(data.to_db()).inserted_id
        return data_id
    
    def get_users(self):
        client = MongoClient()
        db = client[self.DB_NAME]
        table = db["admin_users"]
        return [user['username'] for user in table.find({})]
    
    def save_user(self, username):
        client = MongoClient()
        db = client[self.DB_NAME]
        table = db["admin_users"]

        if table.find_one({"username": username}) is None:
            table.insert_one({"username": username})