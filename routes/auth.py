from flask import Blueprint
from flask import render_template, request, redirect, url_for
from flask_login import login_user, login_required, logout_user
from models import User, db

auth_bp = Blueprint("auth", __name__)

# Register Route
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Always compares the method type
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            username = data['username']
            nickname = data['nickname']
            email = data['email']
            password = data['password']
            gender = data['gender']
            age = data['age']

        else:
            username = request.form['username']
            nickname = request.form['nickname']
            email = request.form['email']
            password = request.form['password']
            gender = request.form['gender']
            age = request.form['age']

        # Checking if the nickname is already in use
        if User.query.filter_by(nickname=nickname).first():
            return 'Este nickname já está em uso'

        # Inserting information into the users table
        user = User(username=username, nickname=nickname, email=email, gender=gender, age=age)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        # Login user method
        login_user(user)
        token = request.cookies.get('session')
        return redirect(url_for('views.index')), 200 

    return render_template('register.html')

# Login Route
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Always compares the method type
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            nickname = data['nickname']
            password = data['password']
        else:
            nickname = request.form['nickname']
            password = request.form['password']

        user = User.query.filter_by(nickname=nickname).first()

        # Checking if the password is correct
        if user and user.check_password(password):
            login_user(user)
            token = request.cookies.get('session')
            return redirect(url_for('views.index'))

        else:
            return 'O nickname ou a senha estão incorretos'

    return render_template('login.html')

# Logout Route
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))