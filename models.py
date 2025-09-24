from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, UTC

db = SQLAlchemy()
class User(UserMixin, db.Model):
    # Table Columns
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    nickname = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    gender = db.Column(db.String(80), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    # Table Methods
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Workspace(db.Model):
    # Table Columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now(UTC))

    # Table Relationships
    members = db.relationship('WorkspaceMember', backref='workspace', lazy=True)
    boards = db.relationship('Board', backref='workspace', lazy=True)

class WorkspaceMember(db.Model):
    # Table Columns
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.id'))
    role = db.Column(db.String(20), default='member') ##Owner, Admin, Member...

    # Table Relationships
    user = db.relationship('User', backref='workspacemember')

class Board(db.Model):
    # Table Columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    about = db.Column(db.Text)
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.id'))
    created_date = db.Column(db.DateTime, default=datetime.now(UTC))

    # Table Relationships
    columns = db.relationship('Column', backref='board')

class Column(db.Model):
    # Table Columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    position = db.Column(db.Integer, default=0)

    # Table Relationships
    cards = db.relationship('Card', backref='column', lazy=True, order_by='Card.position')

class Card(db.Model):
    # Table Columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'), nullable=False)
    position = db.Column(db.Integer, default=0)
    column_id = db.Column(db.Integer, db.ForeignKey('column.id'), default=1, nullable=False)
    responsible_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now(UTC), nullable=False)
    deadline = db.Column(db.DateTime)

    # Table Relationships
    responsible_user = db.relationship('User', foreign_keys=[responsible_id])













