import pymongo
from bson import json_util

connessione = pymongo.MongoClient("mongodb://172.17.0.3:27017/")
db = connessione["cloud_routes_db"]
    
def create_users(data):
    collection = db["users"]
    indert_id = collection.insert_one(data)

def read_users(data):
    collection = db["users"]
    criterio = { "username": data['username'] }
    return json_util.dumps(collection.find(criterio))

def update_users(data):
    collection = db["users"]
    criterio = { "username": data['username'] }
    valore = { "$set": { "password": data['password'], "email": data['email'], "city": data['city'] } }    
    collection.update_one(criterio, valore)

def delete_users(data):
    collection = db["users"]
    criterio = { "username": data['username'] }
    collection.delete_one(criterio)
