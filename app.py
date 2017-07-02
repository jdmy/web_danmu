# -*- coding: UTF-8 -*-
from __future__ import unicode_literals
import time
import socket
import threading
from flask import (Flask, render_template, g, session, redirect, url_for,
                   request, flash,current_app)
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

def tcplink(sock, addr):
    print('Accept new connection from %s:%s...' % addr)
    sock.send(b'Welcome!')
    while True:
        time.sleep(1)
        with app.app_context():
            if not current_app.danmu_queue.empty():
                sock.send(current_app.danmu_queue.get(block=False).encode("utf-8"))
    sock.close()
    print('Connection from %s:%s closed.' % addr)

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


@app.route('/admin', methods=['GET'])
def admin():
    if request.method == 'GET':
        username = request.args.get("username")
        password = request.args.get("password")
        if username == "admin" and password == "admin":
            # 创建一个socket:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('127.0.0.1', 5001))
            s.listen(10)
            print('Waiting for connection...')

            try:
                # 接受一个新连接:
                sock, addr = s.accept()
                # 创建新线程来处理TCP连接:
                t = threading.Thread(target=tcplink, args=(sock, addr))
                t.start()
            except ConnectionResetError as e:
                print(e)
                sock.close()


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
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
    app.run(host="0.0.0.0")
