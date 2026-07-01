import os
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta
from waitress import serve
from dotenv import load_dotenv

load_dotenv(dotenv_path=".flaskenv", verbose=True)

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.instance_path = os.path.join(os.getcwd())

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=3)
    app.config['REMEMBER_COOKIE_HTTPONLY'] = True
    app.config['REMEMBER_COOKIE_SAMESITE'] = 'Lax'

    db.init_app(app)
    Migrate(app, db)

    try:
        from .models import User
    except ImportError:
        from models import User
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    # User_loader - Used to load the user from userID stored in session
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    try:
        from .main import main as main_blueprint
        from .auth import auth as auth_blueprint
    except ImportError:
        from main import main as main_blueprint
        from auth import auth as auth_blueprint

    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
    
    return app

app = create_app()

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=7010, threads=4, debug=True, reload=True)