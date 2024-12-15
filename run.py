from app.extensions import db, celery, ma
from app.routes import app
from app.admin import admin

app.config.from_object('config.Config')

db.init_app(app)
ma.init_app(app)
celery.init_app(app)
admin.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
