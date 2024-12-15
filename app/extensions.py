from flask_sqlalchemy import SQLAlchemy
from flask_celery import Celery
from flask_marshmallow import Marshmallow
from flask_admin import Admin

db = SQLAlchemy()
celery = Celery()
ma = Marshmallow()
admin = Admin(name='Dashboard', template_mode='bootstrap3')
