from flask import render_template, g, request, redirect, url_for

import psycopg2.extras

from app import app


# ~~~~
@app.before_request
def before_request():
    g.db = psycopg2.connect('dbname=flask-practice user=flask password=flask host=127.0.0.1')


@app.teardown_request
def teardown_request(exception):
    g.db.close()


# ~~~~

@app.route('/')
def index():
    title = "Olá Mundo"
    paragraph = "Este é o primeiro teste sem preconceito com flask"
    return render_template('home.html', title=title, paragraph=paragraph)


@app.route('/users', methods=['GET'])
def users():
    cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)

    cur.execute("SELECT * FROM users")

    data = cur.fetchall()
    cur.close()

    return render_template('users.html', users=data)


@app.route('/user/new', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        print(request.form['name'])
        cur = g.db.cursor()
        cur.execute(f"INSERT INTO users(name) VALUES('{request.form['name']}')")
        g.db.commit()
        cur.close()
        return redirect(url_for('users'))
    return render_template('form.html')


@app.route('/user/<int:pk>', methods=['GET'])
def detail_user(pk):
    cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(f"SELECT * FROM users WHERE id = {pk}")
    user = cur.fetchone()
    cur.close()
    return render_template('detail.html', id=user[0], name=user[1])


@app.route('/user/<int:pk>/edit', methods=['GET', 'POST'])
def edit_user(pk):
    cur = g.db.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == "POST":
        cur.execute(f"UPDATE users SET name='{request.form['name']}' WHERE id={pk}")
        g.db.commit()
        cur.close()
        return redirect(url_for('users'))
    cur.execute(f"SELECT name FROM users WHERE id = {pk}")
    name = cur.fetchone()['name']
    return render_template('form.html', name=name)
