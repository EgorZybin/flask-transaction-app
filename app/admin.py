from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from .models import User, Transaction
from .extensions import db


class UserModelView(ModelView):
    can_delete = True
    column_filters = ['role']
    form_columns = ['balance', 'commission_rate', 'role']


class TransactionModelView(ModelView):
    column_filters = ['status', 'user_id']
    form_columns = ['amount', 'commission', 'status']


admin = Admin(name='Dashboard', template_mode='bootstrap3')
admin.add_view(UserModelView(User, db.session))
admin.add_view(TransactionModelView(Transaction, db.session))
