from flask import Blueprint, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

try:
    from .models import User
    from . import db
except ImportError:
    from models import User
    from __init__ import db


auth = Blueprint("auth", __name__)

@auth.route("/signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template("signin.html")
    
    if request.method == 'POST':
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            print("User already exists")
            return redirect(url_for('auth.signin'))
        
        new_user = User(name=name, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        remember = True if request.form.get("remember") else False

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            print("Invalid email or password")
            return redirect('auth.login')
        
        login_user(user, remember=remember)
        return redirect(url_for('main.profile'))
        
@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))