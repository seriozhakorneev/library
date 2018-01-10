from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Configuration
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
# редирект роут для незалогининого пользователя
login_manager.login_view = 'books'