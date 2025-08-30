from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Workspace, WorkspaceMember, Board, Column, Card
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productivity.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

##Loading user informations
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

##Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    ##Always compares the method type
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

        ##Checking if the nick name is already in use
        if User.query.filter_by(nickname=nickname).first():
            return 'Este nickname já está em uso'

        ##Inserting information into the users table
        user = User(username=username, nickname=nickname, email=email, gender=gender, age=age)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        ##Login user method
        login_user(user)

        return jsonify({"message:": "Êxito no cadastro", "User ID:": user.id, "User:": username}), 200 ###, redirect(url_for('base.html'))

    return render_template('register.html')

##Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    ##Always compares the method type
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            nickname = data['nickname']
            password = data['password']
        else:
            nickname = request.form['nickname']
            password = request.form['password']

        user = User.query.filter_by(nickname=nickname).first()

        ##Checking if the password is correct
        if user and user.check_password(password):
            login_user(user)
            return jsonify({"message:": "Êxito no login", "User ID:": user.id, "User:": nickname}) ###, redirect(url_for('base.html'))'''

        else:
            return 'O nickname ou a senha estão incorretos'

    return render_template('login.html')

##Logout Route
@app.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('login.html'))

##Workspace Creation Route
@app.route('/create_workspace', methods=['GET', 'POST'])
@login_required
def create_workspace():
    ##Always compares the method type
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
            title = data['title']
            description = data['description']

        else:
            title = request.form['title']
            description = request.form['description']

        if title == None:
            return jsonify({"message:": "É obrigatório informar um título"}), 400

        owner_id = current_user.id

        workspace = Workspace(title=title, description=description, owner_id=owner_id)
        db.session.add(workspace)
        db.session.commit()

        ##Adding the workspace owner as a member
        workspace_member = WorkspaceMember(user_id=current_user.id, workspace=workspace, role='Owner')
        db.session.add(workspace_member)
        db.session.commit()

        return jsonify({"message:": "Workspace criado com sucesso."}), 200

    return render_template('base.html')

##Workspace Access
@app.route('/workspace/<int:workspace_id>')
@login_required
def workspace(workspace_id):
    ##Looking for an workspace that matches the passed id
    workspace = Workspace.query.get_or_404(workspace_id)

    ##Checking the users access
    if not WorkspaceMember.query.filter_by(user_id=current_user.id, workspace_id=workspace_id).first():
        return jsonify({"message:": "Acesso negado"}), 403

    ##Getting boards and members from the workspace
    boards = Board.query.filter_by(workspace_id=workspace_id)
    members = User.query.join(WorkspaceMember).filter(WorkspaceMember.workspace_id == workspace_id).all()

    return render_template('workspace.html',
                                            workspace=workspace,
                                            boards=boards,
                                            members=members)

##Board Creation Route
@app.route('/workspace/<int:workspace_id>/create_board', methods=['POST'])
@login_required
def create_board(workspace_id):
    ##Looking for an workspace that matches the passed id
    workspace = Workspace.query.get_or_404(workspace_id)

    ##Checking the users access
    if not WorkspaceMember.query.filter_by(user_id=current_user, workspace_id=workspace_id).first():
        return jsonify({"message:": "Acesso negado"}), 403

    ##Always compares the method type
    if request.is_json:
        data = request.get_json()
        title = data['title']
        about = data['about']

    else:
        title = request.form['title']
        about = request.form['about']

    if title == None:
        return jsonify({"message:": "É obrigatório informar um título."}), 400

    ##Adding the board
    board = Board(title=title, about=about, workspace_id=workspace_id)
    db.session.add(board)
    db.session.commit()

    ##Adding the default columns
    default_columns = ['To Do', 'Doing', 'Done']

    for i in default_columns:
        column = Column(title=default_columns[i], board_id=board.id, position=i)
        db.session.add(column)

    db.session.commit()

    ##Returning to the endpoint that shows the workspaces
    return redirect(url_for('workspace', workspace_id=workspace_id))

##Workspace Listing Route
@app.route('/listar_workspace')
@login_required
def listar_workspace():
    ##Searching for workspaces owned by the current user
    workspaces_one = Workspace.query.filter_by(owner_id=current_user.id).all()
    ##Searching for workspaces that the current user is a member of.
    workspaces_two = Workspace.query.join(WorkspaceMember).filter(WorkspaceMember.user_id == current_user.id).all()

    ##Merging both queries
    workspaces = list(set(workspaces_one + workspaces_two))

    lista_workspaces = []

    ##Creating a list to organize the data
    for wkspace in workspaces:
        lista_workspaces.append({
            'id': wkspace.id,
            'title': wkspace.title,
            'description': wkspace.description,
            'owner_id': wkspace.owner_id,
            'created_date': wkspace.created_date
        })

    return jsonify(lista_workspaces)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

