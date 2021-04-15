import pymongo
from bson import json_util

connessione = pymongo.MongoClient("mongodb://172.17.0.3:27017/")
db = connessione["cloud_routes_db"]

def create_routes(data):
    collection = db["routes"]
    indert_id = collection.insert_one(data)

def read_routes(data):
    collection = db["routes"]
    if data['routes_id']:
        criterio = { "routes_id": data['routes_id'] }
    else:
        criterio = { "username": data['username'], "date": data['date'], "city": data['city'] }
    
    return json_util.dumps(collection.find(criterio))

def update_routes(data):
    collection = db["routes"]
    if data['routes_id']:
        criterio = { "routes_id": data['routes_id'] }
    else:
        criterio = { "username": data['username'], "date": data['date'], "city": data['city'] }
    valore = { "$set": { "city": data['city'], "route": data['route'] } }    
    collection.update_one(criterio, valore)

def delete_routes(data):
    collection = db["routes"]
    criterio = { "routes_id": data['routes_id'] }
    collection.delete_one(criterio)
