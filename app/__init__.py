from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask.json import JSONEncoder
from flask_marshmallow import Marshmallow
from datetime import date

# custom JSON encoder to change date format to 'yyyy-mm-dd'
class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
app.config['SECRET_KEY'] = '389c4704e2873f77fa5ecad8fe3e4046e1925c4d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///team_wilson.db'
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
ma = Marshmallow(app)



from app import routes