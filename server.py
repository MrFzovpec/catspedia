from flask import Flask, render_template, request, session, redirect, url_for
import json
import datetime
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'jrfasefasefgj'

client = MongoClient('mongodb://Petr:GPpetr1309@cluster0-shard-00-00-nli2o.mongodb.net:27017,cluster0-shard-00-01-nli2o.mongodb.net:27017,cluster0-shard-00-02-nli2o.mongodb.net:27017/cats?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')
db = client['catspedia']
collection = db.cats
cats = collection.find()
users_collection = db.users
users = users_collection.find()

@app.route('/wall', methods=['GET'])
def index():
    if session.get('auth', False) == True:
        cats = collection.find()
        username = session['username']
        return render_template('index.html', cats=cats, User=username)
    else:
        return redirect('/')


@app.route('/add', methods=['GET'])
def add_form():
    return render_template('add.html', User=session['username'])


@app.route('/add', methods=['POST'])
def add():
    if session.get('auth', False) == False:
        return redirect('/')
    else:
        fields = ['name', 'photo', 'description']
        for field in fields:
            if request.form.get(field, '') == '':
                return redirect('/add')
        cat = {
            "name": request.form['name'],
            "author": session['username'],
            "description": request.form['description'],
            "short_description": request.form['short_description'],
            "photo": request.form['photo'],
            "comments": [],
            "liked": [],
            "likes": 0
        }
        collection.insert_one(cat)
        return redirect('/cats/{0}'.format(cats.count()))

@app.route('/edit/<id>', methods=['GET'])
def edit(id):
    cats = collection.find()
    cat = cats[int(id)-1]
    if session['username'] == cat['author']:
        return render_template('edit.html', cat=cat, User=session['username'])
    else:
        return redirect('/cats/'+str(id))
@app.route('/edit/<id>', methods=['POST'])
def edit_2(id):
    cats = collection.find()
    cat = cats[int(id)-1]
    cat["name"] = request.form['name']
    cat["description"] = request.form['description']
    cat["short_description"] = request.form['short_description']
    cat["photo"] = request.form['photo']
    id_send = { "_id": cat['_id'] }
    collection.update_one(id_send, {"$set":cat})
    return redirect('/cats/' + id)
@app.route('/cats/<id>', methods=['GET'])
def details(id):
    button_delete = ""
    if session.get('auth', False) == False:
        return redirect('/')
    else:

        button_delete = "display: none"
        cats = collection.find()
        cat = cats[int(id) - 1]

        session['id_cat'] = int(id) - 1
        session['pos_cat'] = int(id)
        username = session['username']
        if username not in cat['liked']:
            text_like = "Поставить лайк"
        else:
            text_like = "Убрать лайк"
        if cat['author'] == username:
            button_delete = "display: block"
        else:
            button_delete = "display: none"
        return render_template('details.html', cat=cat, id=id, User=username, style=button_delete, text_like=text_like)
@app.route('/cats/delete_comment/<id>', methods=['POST'])
def comment_delete(id):
    cats = collection.find()
    cat = cats[session['id_cat']]
    comments = cat['comments']
    for com in comments:
        if com['id'] == int(id):
            comment = com
    if comment['author'] == session['username']:
        comments.remove(comment)
        id_send = { "_id": cat['_id'] }
        collection.update_one(id_send, {"$set":cat})
    return redirect('/cats/' + str(session['id_cat']+1))

@app.route('/cats/<id>/delete', methods=['GET'])
def delete(id):

    collection.delete_one(cats[int(id)-1])
    return redirect('/')
@app.route('/like/<id>', methods=['GET'])
def like(id):
    if session.get('auth', False) == False:
        return redirect('/')
    else:
        cats = collection.find()
        cat = cats[int(id) - 1]
        if session['username'] not in cat['liked']:
            cat['likes'] += 1
            cat['liked'].append(session['username'])

        else:
            cat['likes'] -= 1
            cat['liked'].remove(session['username'])
        id_send = { "_id": cat['_id'] }
        collection.update_one(id_send, {"$set":cat})
        return redirect('/cats/{0}'.format(int(id)))


@app.route('/comment/<id>', methods=['POST'])
def comment(id):
    if session.get('auth', False) == False:
        return redirect('/')
    else:
        username = session['username']
        cats = collection.find()
        cat = cats[int(id) - 1]
        whole_time = datetime.datetime.now()
        fields = ['text']
        for field in fields:
            if request.form.get(field, '') == '':
                return redirect('/')
        comment = {
            "id": len(cat['comments'])+1,
            "author": username,
            "text": request.form['text'],
            "date": str(whole_time.date())+"\n"+ str(whole_time.hour) + ":" + str(whole_time.minute),
        }
        cat['comments'].append(comment)
        id_send = { "_id": cat['_id'] }
        collection.update_one(id_send, {"$set":cat})
        return redirect('/cats/{0}'.format(int(id)))
@app.route('/')
def secret():
    if session.get('auth', False) == True:
        return redirect('/wall')
    else:
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    login = request.form['login']
    print(login)
    password = request.form['password']
    print(password)
    if (users_collection.count({'login': login}) == 1) or (users_collection.count({'email': login}) == 1):
        user = users_collection.find_one({'login': login})
        if user['password'] == password:
            session['auth'] = True
            session['username'] = login
            return redirect('/')
        else:
            return render_template('login.html', Error="Неправильный логин или пароль")
    else:
        return render_template('login.html', Error="Неправильный логин или пароль")

@app.route('/signup', methods=['POST'])
def signup():
    user = {
        'login': request.form['login'],
        'password': request.form['password'],
        'email': request.form['email'],
        'country': request.form['country']
    }
    if users_collection.count({'login': user['login']}) == 0:
        if users_collection.count({'email': user['email']}) == 0:
            users_collection.insert_one(user)
            session['auth'] = True
            session['username'] = user['login']
            return redirect('/')
        else:
            return render_template('signup.html', Error="Такой Email уже зарегистрирован!", login="Войти?")
    else:
        return render_template('signup.html', Error="Такой логин уже зарегистрирован в системе! Придумайте другой!", login="Войти?")

@app.route('/signup')
def sign():
    return render_template('signup.html')
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
app.run(debug=True, port=8080)
