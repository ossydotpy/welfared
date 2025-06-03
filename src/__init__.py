from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from config import config
import os

load_dotenv()

env = os.getenv('DEP_STAGE', 'dev')

app = Flask(__name__)
app.config.from_object(config[env]) 

# security stuff
bcrypt = Bcrypt(app)

# db stuff
db = SQLAlchemy(app)
migrate = Migrate(app=app, db=db)


# login stuff
login_manager = LoginManager(app)
login_manager.init_app(app=app)

login_manager.login_view = "accounts.login"
login_manager.login_message_category = "info"

# blueprint stuff
from src.accounts.views import accounts_bp
from src.core.views import core_bp

app.register_blueprint(accounts_bp, url_prefix='/accounts')
app.register_blueprint(core_bp, url_prefix='/')


from src.models import User

@login_manager.user_loader
def load_user(id):
    return User.query.filter(User._id == int(id)).first()