drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title text not null,
  'text' text not null
);
drop table if exists users;
create table users (
  id integer primary key autoincrement,
  username text not null,
  password text not null,
  fToken text,
  tToken text,
  tkey text,
  tsecret1 text,
  tsecret2 text
  );
CREATE TABLE IF NOT EXISTS FB
				   (id TEXT NOT NULL PRIMARY KEY UNIQUE,
					name TEXT,
					createTime TEXT,
					message TEXT );
					
CREATE TABLE IF NOT EXISTS Twitter 
				   (tweet TEXT, 
					createTime TEXT, 
					user TEXT, 
					id INTEGER NOT NULL PRIMARY KEY UNIQUE);