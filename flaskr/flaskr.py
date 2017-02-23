# -*- coding: utf-8 -*-

import time
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
	 render_template, flash

from twitterApi import *
from FBGetter import *
app = Flask(__name__)


# Load default config and override config from an environment variable
app.config.update(dict(
	DATABASE=os.path.join(app.root_path, 'flaskr.db'),
	DEBUG=True,
	SECRET_KEY='development key',
	USERNAME='admin',
	PASSWORD='default'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
start = time.clock()

def connect_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv


def init_db():
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()


@app.cli.command('initdb')
def initdb_command():
	init_db()
	print('Initialized the database.')


def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()



@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	
	if request.method == 'POST':
		db = get_db()
		cur=db.execute('select password from users where username=?',[request.form['username']])
		
		password=cur.fetchone()[0]
		print(password)
		if request.form['password'] != password or password==None:
			error = 'Invalid password'
		else:
			session['logged_in'] = True
			return redirect(url_for('get_twitter'))
	return render_template('login.html', error=error)

@app.route('/show_register')
def show_register():
	return render_template('register.html' )

@app.route('/register', methods=['POST'])
def register():
	error = None
	if request.method == 'POST':
		db = get_db()
		db.execute('insert into users (username, password) values (?, ?)',[request.form['username'], request.form['password']])
		db.commit()
		session['logged_in'] = True
		flash('You were logged in')
		return redirect(url_for('get_twitter'))
	return render_template('login.html', error=error)
		

@app.route('/')
def index():
	return redirect(url_for('login'))
		

@app.route('/twitter')
def get_twitter():
	if 'logged_in' not in session:
		return redirect(url_for('login'))
	else:
		get_home_timeline()
		db = get_db()
		cur = db.cursor()
		cur.execute('select * from Twitter order by id desc')
		tweets = cur.fetchall()
	#tweets=get_home_timeline()
	#for row in cur:
	#print(cur.fetchall())
		return render_template('twitter.html',posts=tweets)
	
@app.route('/facebook')
def get_facebook():
	if 'logged_in' not in session:
		return redirect(url_for('login'))
	else:
		last_refresh = start
		if time.clock() - last_refresh >100:
			last_refresh = time.clock()
			invokeFB(app)
		db = get_db()
		cur = db.cursor()
		cur.execute('select * from FB order by createTime desc')
		tweets = cur.fetchall()
	#tweets=get_home_timeline()
	#for row in cur:
	#print(cur.fetchall())
		return render_template('facebook.html',posts=tweets)

@app.route('/logout')
def logout():	
	flash('You were logged out')
	return redirect(url_for('login'))
