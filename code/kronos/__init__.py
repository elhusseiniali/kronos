from flask import Flask

from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from flask_restplus import Api

app = Flask(__name__)
app.config['SECRET_KEY'] = '60808326457a6384f78964761aaa161c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'


api = Api(app, version='1.0', title='Kronos',
          description='A simple scheduling tool.')
conf = api.namespace('schedule', description='All operations.')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


#   Below import is necessary, even if the linter complains about it.
#   This is because the linter cannot distinguish between imports in a script
#   and imports in a package. The order of the imports is also important.
#   These two imports *had* to happen after initializing db.
from kronos import routes
from kronos.models import User, Performer

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


# set optional bootswatch theme
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'

admin = Admin(app, name='Kronos Admin', template_mode='bootstrap3')
# Add administrative views here
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Performer, db.session))
