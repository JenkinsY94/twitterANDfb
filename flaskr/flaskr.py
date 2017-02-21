# -*- coding: utf-8 -*-


import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
	 render_template, flash

from twitterApi import *

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


def connect_db():
	"""Connects to the specific database."""
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv


def init_db():
	"""Initializes the database."""
	db = get_db()
	with app.open_resource('schema.sql', mode='r') as f:
		db.cursor().executescript(f.read())
	db.commit()


@app.cli.command('initdb')
def initdb_command():
	"""Creates the database tables."""
	init_db()
	print('Initialized the database.')


def get_db():
	"""Opens a new database connection if there is none yet for the
	current application context.
	"""
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
	return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
	"""Closes the database again at the end of the request."""
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()


@app.route('/')
def show_entries():
	db = get_db()
	cur = db.execute('select title, text from entries order by id desc')
	entries = cur.fetchall()
	return render_template('show_entries.html', entries=entries)

@app.route('/t')
def show_t():
	return render_template('t.html')

@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	db = get_db()
	db.execute('insert into entries (title, text) values (?, ?)',
			   [request.form['title'], request.form['text']])
	db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))


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
			flash('You were logged in')
			return redirect(url_for('show_entries'))
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
		return redirect(url_for('show_entries'))
	return render_template('login.html', error=error)
		
		

@app.route('/twitter')
def get_twitter():
	db = get_db()
	cur = db.cursor()
	cur.execute('select * from Twitter order by id desc')
	tweets = cur.fetchall()
	#tweets=get_home_timeline()
	#for row in cur:
	#print(cur.fetchall())
	return render_template('twitter.html',posts=tweets)

@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('You were logged out')
	return redirect(url_for('show_entries'))
