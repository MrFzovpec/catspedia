from flask import Flask, render_template, request, redirect
import json
import datetime

app = Flask(__name__)

file = open('cats.json', 'r')
text = file.read()
cats = json.loads(text)

file.close()


@app.route('/', methods=['GET'])
def index():
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
    cats.append(cat)
    file = open('cats.json', 'w')
    file.write(json.dumps(cats))
    file.close()
    return redirect('/cats/{0}'.format(len(cats)))


@app.route('/cats/<id>', methods=['GET'])
def details(id):
    file = open('cats.json', 'r')
    text = file.read()
    cats = json.loads(text)
    file.close()
    cat = cats[int(id) - 1]
    return render_template('details.html', cat=cat, id=id)


@app.route('/like/<id>', methods=['GET'])
def like(id):
    file = open('cats.json', 'r')
    text = file.read()
    text = json.loads(text)
    file.close()
    cat = text[int(id) - 1]
    cat['likes'] += 1
    file = open('cats.json', 'w')
    file.write(json.dumps(text))
    file.close()
    return redirect('/cats/{0}'.format(int(id)))


@app.route('/comment/<id>', methods=['POST'])
def comment(id):
    file = open('cats.json', 'r')
    text = file.read()
    text = json.loads(text)
    file.close()
    cat = text[int(id) - 1]
    whole_time = datetime.datetime.now()
    comment = {
        "author": request.form['author'],
        "text": request.form['text'],
        "date": str(whole_time.date())+"\n"+ str(whole_time.hour) + ":" + str(whole_time.minute),
    }
    cat['comments'].append(comment)
    file = open('cats.json', 'w')
    file.write(json.dumps(text))
    file.close()
    return redirect('/cats/{0}'.format(int(id)))


app.run(debug=True, port=8080)
