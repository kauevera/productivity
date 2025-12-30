from flask import Flask, redirect, url_for, jsonify
from flask_login import LoginManager
from models import db, User
from flask_cors import CORS
from routes.auth import auth_bp
from routes.api import api_bp
from routes.views import views_bp

app = Flask(__name__)

# Creating blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(api_bp, url_prefix="/api")
app.register_blueprint(views_bp, url_prefix="/views")

CORS(app)
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productivity.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Loading user details
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home Route
@app.route('/')
def home():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
