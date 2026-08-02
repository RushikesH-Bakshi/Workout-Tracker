from flask import Blueprint, render_template, url_for, request, redirect, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

try:
    from .models import User
    from . import db
except ImportError:
    from models import User
    from __init__ import db


auth = Blueprint("auth", __name__)

def _get_request_payload():
    if request.is_json:
        return request.get_json(silent=True) or {}
    return request.form


@auth.route("/api/signin", methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template("signin.html")

    if request.method == 'POST':
        data = _get_request_payload()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")

        if not name or not email or not password:
            return jsonify({"message": "Name, email, and password are required"}), 400

        user = User.query.filter_by(email=email).first()

        if user:
            return jsonify({"message": "User already exists"}), 409

        new_user = User(name=name, email=email, password=generate_password_hash(password, method='pbkdf2:sha256'))

        db.session.add(new_user)
        db.session.commit()

        if request.is_json:
            return jsonify({"message": "User created successfully", "user": {"id": new_user.id, "name": new_user.name, "email": new_user.email}}), 200

        return redirect(url_for('auth.login'))

@auth.route("/api/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        data = _get_request_payload()
        email = data.get("email")
        password = data.get("password")
        remember_value = data.get("remember", False)
        remember = remember_value in (True, "true", "True", "on", "1", 1)

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return jsonify({"message": "Invalid email or password"}), 401

        login_user(user, remember=remember)

        if request.is_json:
            return jsonify({"message": "Login successful", "user": {"id": user.id, "name": user.name, "email": user.email}}), 200

        return redirect(url_for('main.profile'))

@auth.route("/api/logout")
@login_required
def logout():
    logout_user()
    if request.is_json:
        return jsonify({"message": "Logout successful"}), 200
    return redirect(url_for('main.home'))