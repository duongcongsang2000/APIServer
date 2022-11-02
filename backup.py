import random
import time
import json

import pymongo
from pymongo import MongoClient
from pymongo import collection
from bson import json_util
import requests

# Thay url mongodb
# cluster = MongoClient("mongodb+srv://haku:Haku2000@cluster0.5zdem.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
cluster = MongoClient("mongodb://localhost:27017")

db = cluster['monitor']         # Database 
collection = db["seeds"]        # Collection

# Lay tat ca gia tri
def get_seeds():
    all_seeds = list(collection.find({}))
    return json.dumps(all_seeds, default=json_util.default)

# Lay gia tri moi nhat
def get_one():
    # all_seeds = list(collection.find().skip(collection.count() -1))
    all_seeds = list(collection.find().sort('_id', -1).limit(1))
    # return json.dumps(all_seeds, default=json_util.default)
    return json.dumps(all_seeds, default=json_util.default)

# Them moi gia tri
def add_seeds(url):
    # Get all hash 
    data = get_data(url)
    # Get last hash in mongodb
    last_element =  json.loads(get_one())
    index = 1
    try:
        print("Lasthash:", last_element[0]['lastHash'])
    except:
        print("Lashhash null")

    if len(last_element) != 0:
        last_hash = last_element[0]['lastHash']
        print("Last hash")
        for idx, i in reversed(list(enumerate((data)))):
            # print(i['lash'])
            if i['lastHash'] == last_hash:
                index = idx+1
                print("lashHash in ", index)
                break

    list_result = []
    for idx, i in list(enumerate(data[index:])):
        # print(i)
        # print(type(i['data']))
        # print(i['data'][0])
        # for x in i['data']:
        #     print(x)
        # exit()
        result = {
            "hash": i['hash'],
            "lastHash": i['lastHash'],
            "input": {
                "timestamp": i['data'][0]['input']['timestamp'],
                "address": i['data'][0]['input']['address'],
            },
            "output": {
                "cpu": i['data'][0]['outputs'][0]['cpu'],
                "ram": i['data'][0]['outputs'][0]['ram'],
                "disk": i['data'][0]['outputs'][0]['disk'],
                "address": i['data'][0]['outputs'][0]['address']
            }
        }
        list_result.append(result)

    if len(list_result) != 0:
        collection.insert_many(list_result)
        print(f"add {len(list_result)} to database")

def get_data(url):

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.json()

if __name__ == '__main__':
    with open('config.json', 'r') as f:
        data = json.load(f)
        host = data['host']
        sleep = data['sleep']
    while True:
        add_seeds(host)
        time.sleep(sleep*6)
    #     TIME, CPU, RAM, DISK = get_computer_info()
    #     add_info(host, TIME, CPU, RAM, DISK)
    
    # print(get_seeds())
    # print(get_one())
    # print(get_data(host))
 