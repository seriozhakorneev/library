from flask_login import UserMixin
from app import db

class Reader(UserMixin, db.Model):
	""" пользователь """
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), unique=True)
	password = db.Column(db.String(100))

# связь книг и авторов
many = db.Table('many',
    db.Column('author_id', db.Integer, db.ForeignKey('author.author_id')),
    db.Column('book_id', db.Integer, db.ForeignKey('book.book_id'))
    )

class Author(db.Model):
	""" автор """
	author_id = db.Column(db.Integer, primary_key=True)
	author_name = db.Column(db.String(100), unique=True)
	writers = db.relationship('Book', secondary=many,
				backref=db.backref('writers', lazy='dynamic'))

class Book(db.Model):
	""" книга """
	book_id = db.Column(db.Integer, primary_key=True)
	book_name = db.Column(db.String(100), unique=True)
