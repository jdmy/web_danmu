from __future__ import unicode_literals
from flask import (Flask, render_template, g, session, redirect, url_for,
                   request, flash, current_app)
from forms import DanmuForm
from flask_bootstrap import Bootstrap
from flask_script import Manager
import queue

SECRET_KEY = 'This is my key'

app = Flask(__name__)
manager = Manager(app)

bootstrap = Bootstrap(app)

app.secret_key = SECRET_KEY
app.config['USERNAME'] = 'admin'
app.config['PASSWORD'] = 'admin'
with app.app_context():
    current_app.danmu_queue = queue.Queue()
    current_app.danmu_list = []


@app.route('/', methods=['GET', 'POST'])
def show_todo_list():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    form = DanmuForm()
    if request.method == 'GET':
        return render_template('index.html', form=form)
    else:
        if form.validate_on_submit():
            content = form.content.data
            with app.app_context():
                print(content)
                current_app.danmu_queue.put(content)
                current_app.danmu_list.append(content)
            flash('吐槽完毕，' + content)
        else:
            flash(form.errors)
        return redirect(url_for('show_todo_list'))


@app.route('/danmu_get', methods=['GET'])
def danmu_get():
    if request.method == 'GET':
        with app.app_context():
            if not current_app.danmu_queue.empty():
                return current_app.danmu_queue.get(block=False)
    return "no"


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            flash('Invalid username')
        elif request.form['password'] != app.config['PASSWORD']:
            flash('Invalid password')
        else:
            session['logged_in'] = True
            flash('you have logged in!')
            return redirect(url_for('show_todo_list'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('you have logout!')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run()
