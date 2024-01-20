from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = '689567gh$^^&*#%^&*^&%^*DFGH^&*&*^*'
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:%s@localhost/qlhs?charset=utf8mb4' % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_RECORD_QUERIES"] = True
app.config["PAGE_SIZE"] = 6

cloudinary.config(cloud_name='dkfnlesea', api_key='841397193959693', api_secret='ZbKiAJ_qnDGZt1bfkIei9hRgceA')

db = SQLAlchemy(app=app)
login = LoginManager(app=app)

