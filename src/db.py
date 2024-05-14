from pymongo import MongoClient
from data import Data



class Db(object):

    def __init__(self, DB_NAME, MONGODB_CONTAINER_NAME):
        self.client = MongoClient(MONGODB_CONTAINER_NAME, port=27017)
        self.db = self.client[DB_NAME]

    # Letölti az összes képet ami a megadott felhasználóhoz tartozik.
    def download_all(self, username):
        table = self.db[username]

        images = table.find()
        
        datas = []
        for image in images:
            datas.append(Data.from_db(image))

        return datas
    
    # Letölti a megadott nevű képet ami a megadott felhasználóhoz tartozik.
    def download(self, username, filename):
        table = self.db[username]

        image = table.find_one({"filename":filename})
        return Data.from_db(image)
    
    # Elmenti a felhasználó által feltöltött képet az adataival együtt.
    def upload(self, username, data):
        table = self.db[username]

        data_id = table.insert_one(data.to_db()).inserted_id
        return data_id
    
    # Az visszaadja az összes eddig bejelentkezett felhasználó nevét.
    def get_users(self):
        table = self.db["admin_users"]
        return [user['username'] for user in table.find({})]
    
    # Az elmenti egy felhasználó nevét.
    def save_user(self, username):
        table = self.db["admin_users"]

        if table.find_one({"username": username}) is None:
            table.insert_one({"username": username})