import os

class Configuration():
	DEBUG = False
	SECRET_KEY = 'my1_1s1e3c5r6e7t_ke2y'
	SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
	SQLALCHEMY_TRACK_MODIFICATIONS = False
