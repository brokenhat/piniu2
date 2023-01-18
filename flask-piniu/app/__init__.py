from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_pure import Pure
from flask_ckeditor import CKEditor
from flask_mail import Mail
from celery import Celery

# these objects initialise extensions which are imported above
app = Flask(__name__)
app.config.from_object(Config)
mail = Mail()

celery = Celery(app, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# |||||||||||||||||||||||||||||||||
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
pure = Pure(app)
ckeditor = CKEditor(app)
mail.init_app(app)

from app import routes, models
# module models defines structure of database
