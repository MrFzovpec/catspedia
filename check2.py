from pymongo import MongoClient
from flask import Flask, request
import json
import ssl
import pprint


app = Flask(__name__)
client = MongoClient('mongodb://Petr:GPpetr1309@cluster0-shard-00-00-nli2o.mongodb.net:27017,cluster0-shard-00-01-nli2o.mongodb.net:27017,cluster0-shard-00-02-nli2o.mongodb.net:27017/cats?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')
db = client['catspedia']
collection = db.cats
cats = [
    {

        "name": "Гуся",
        "photo": "https://memepedia.ru/wp-content/uploads/2019/03/dxdaey6uuaakpup-kopiya.jpg",
        "description": "Любит вкусно поесть гусей.",
        "short_description": "Красивый код",
        "comments": [
            {
                "author": "Александр",
                "text": "*людей...)))",
                "date": "13.37.28"
            }
        ],
        "likes": 6

    }
]
for cat in cats:
    collection.insert_one(cat)
all_cats = collection.find()

for cat in all_cats:
    print(cat)
