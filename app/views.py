from flask import render_template

from app import app


@app.route('/')
def index():
    title = "Olá Mundo"
    paragraph = "Este é o primeiro teste sem preconceito com flask"
    return render_template('base.html', title=title, paragraph=paragraph)
