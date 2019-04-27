from flask import Flask, render_template, request, redirect
import json
import datetime
from pymongo import MongoClient


app = Flask(__name__)
client = MongoClient('mongodb://Petr:GPpetr1309@cluster0-shard-00-00-nli2o.mongodb.net:27017,cluster0-shard-00-01-nli2o.mongodb.net:27017,cluster0-shard-00-02-nli2o.mongodb.net:27017/cats?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')
db = client['catspedia']
collection = db.cats
cats = collection.find()

@app.route('/', methods=['GET'])
def index():
    cats = collection.find()
    return render_template('index.html', cats=cats)


@app.route('/add', methods=['GET'])
def add_form():
    return render_template('add.html')


@app.route('/add', methods=['POST'])
def add():
    fields = ['name', 'photo', 'description']
    for field in fields:
        if request.form.get(field, '') == '':
            return redirect('/add')
    cat = {
        "name": request.form['name'],
        "description": request.form['description'],
        "short_description": request.form['short_description'],
        "photo": request.form['photo'],
        "comments": [],
        "likes": 0
    }
    return redirect('/cats/{0}'.format(cats.count()))


@app.route('/cats/<id>', methods=['GET'])
def details(id):
    cats = collection.find()
    cat = cats[int(id) - 1]
    return render_template('details.html', cat=cat, id=id)


@app.route('/like/<id>', methods=['GET'])
def like(id):
    cats = collection.find()
    cat = cats[int(id) - 1]
    cat['likes'] += 1
    id_send = { "_id": cat['_id'] }
    collection.update_one(id_send, {"$set":cat})
    return redirect('/cats/{0}'.format(int(id)))


@app.route('/comment/<id>', methods=['POST'])
def comment(id):
    cats = collection.find()
    cat = cats[int(id) - 1]
    whole_time = datetime.datetime.now()
    fields = ['author', 'text']
    for field in fields:
        if request.form.get(field, '') == '':
            return redirect('/cats/<id>')
    comment = {
        "author": request.form['author'],
        "text": request.form['text'],
        "date": str(whole_time.date())+"\n"+ str(whole_time.hour) + ":" + str(whole_time.minute),
    }
    cat['comments'].append(comment)
    id_send = { "_id": cat['_id'] }
    collection.update_one(id_send, {"$set":cat})
    return redirect('/cats/{0}'.format(int(id)))


app.run(debug=True, port=8080)
