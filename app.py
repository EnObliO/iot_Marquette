#!/usr/bin/env python3.5
# -*- coding:utf-8 -*-
from flask import Flask, redirect, url_for
import mysql.connector
from flask import Flask, session
from flask import render_template
from flask import request
from flaskext.mysql import MySQL
from flask import g
from passlib.hash import argon2
app = Flask(__name__)
app.secret_key = 'some random string w17h n|_|m83r5'
def connect_db () :
    g.mysql_connection = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'root',
        database = 'cours_iot_python_pour_le_web'
    )   

    g.mysql_cursor = g.mysql_connection.cursor()
    return g.mysql_cursor


def get_db () :
    if not hasattr(g, 'db') :
        g.db = connect_db()
    return g.db


@app.teardown_appcontext
def close_db (error) :
    if hasattr(g, 'db') :
        g.db.close()

@app.route('/admin/', methods = ['GET', 'POST'])
def admin () :
    if not session.get('user') or not session.get('user')[2] :
        return redirect(url_for('login'))

    site_name = str(request.form.get('site_name'))
    site_url = str(request.form.get('site_url'))
    
    db = get_db()
    #sql = "INSERT INTO entries(name, value) VALUES(%s,%s)", (site_name, site_url)
    try :
      db.execute("INSERT INTO entries(name, value) VALUES(%s, %s)", (site_name, site_url))
      db.commit()
    except :
      dunno = "python ca pue la merde et les sites en python ca pue encore plus la merde !!!!!!!!!!!!!!!!!!!!!!!!!"

    return render_template('admin.html', user = session['user'])


@app.route('/login/', methods = ['GET', 'POST'])
def login () :
    email = str(request.form.get('email'))
    password = str(request.form.get('password'))

    db = get_db()
    db.execute('SELECT email, password, is_admin FROM user WHERE email = %(email)s', {'email' : email})
    users = db.fetchall()

    valid_user = False
    for user in users :
        #if argon2.verify(password, user[1]) :
            valid_user = user
     
    if valid_user :
        session['user'] = valid_user
        return redirect(url_for('admin'))

    return render_template('login.html')


@app.route('/admin/logout/')
def admin_logout () :
    session.clear()
    return redirect(url_for('login'))


@app.route('/show-entries/')
def show_entries () :
    db = get_db()
    db.execute('SELECT name, value FROM entries')
    entries = db.fetchall()
    return render_template('show-entries.html', entries = entries)

@app.route('/')
def index () :
    return 'Hello World !'

@app.route('/show-sentence/<sentence>/')
def show_sentence (sentence) :
    return 'You say : ' + sentence

@app.route('/show-sentence-template/<sentence>/')
def show_sentence_template (sentence) :
    return render_template('show-sentence.html', sentence = sentence)

@app.route('/multiply/<int:first_number>/<int:second_number>/')
def multiply (first_number, second_number) :
    result = first_number * second_number
    return 'Result of {} * {} = {}'.format(first_number, second_number, result)

@app.route('/lorem-ipsum/')
def lorem_ipsum () :
    page = """ 
        <!doctype html>
        <html lang="fr">
        <head>
                <meta charset="utf-8">
                <title>Lorem Ipsum</title>
        </head>
        <body>
                <h1>Lorem Ipsum</h1>
                <p>
                        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque condimentum at lectus at tristique. Ut dignissim congue enim. Ut tempus euismod lacus, eu blandit erat commodo ut. Pellentesque vestibulum, est nec pretium malesuada, mauris libero cursus purus, congue tempor tortor nisl eget augue. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Phasellus ac diam felis. Donec suscipit justo hendrerit ipsum eleifend rutrum. Aliquam dignissim at velit non tristique. Mauris ligula turpis, finibus ut condimentum ut, dapibus vel nulla. Cras imperdiet luctus ex ac placerat. Integer et rhoncus eros, id mattis metus. Vivamus gravida lacus et euismod tempus. 
                </p>
        </body>
        </html> 
    """
    return page

@app.route('/lorem-ipsum-template/')
def lorem_ipsum_template () :
    return render_template('lorem-ipsum.html')


@app.route('/contact/', methods=['GET', 'POST'])
def contact () :
    email = request.form.get('email')
    message = request.form.get('message')
    return render_template('contact.html', email = email, message = message)

if __name__ == '__main__':
    app.run(debug = True)
