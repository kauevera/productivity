from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, login_required, current_user
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

# Loading user details
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home Route
@app.route('/')
def home():
    return redirect(url_for('login'))

# Register Route
@app.route('/register', methods=['GET', 'POST'])
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
        return jsonify({"message:": "Êxito no cadastro", "User ID:": user.id, "User:": username, "Token": token}), 200 ###, redirect(url_for('base.html'))

    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('index'))

        else:
            return 'O nickname ou a senha estão incorretos'

    return render_template('login.html')

# Logout Route
@app.route('/logout')
@login_required
def logout():
    logout()
    return redirect(url_for('login.html'))

# Base Route
@app.route('/index')
@login_required
def index():
    # Looking for all workspaces that the user is member of.
    workspaces = Workspace.query.join(WorkspaceMember).filter(WorkspaceMember.user_id == current_user.id).all()

    return render_template('index.html',
                           workspaces=workspaces)

# Workspace Creation Route
@app.route('/create_workspace', methods=['GET', 'POST'])
@login_required
def create_workspace():
    # Looking for all workspaces that the user is member of.
    workspaces = Workspace.query.join(WorkspaceMember).filter(WorkspaceMember.user_id == current_user.id).all()

    # Always compares the method type
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

        # Adding the workspace owner as a member
        workspace_member = WorkspaceMember(user_id=current_user.id, workspace=workspace, role='Owner')
        db.session.add(workspace_member)
        db.session.commit()

        return jsonify({"message:": "Workspace criado com sucesso."}), 200

    return render_template('index.html',
                           workspaces=workspaces)

# Workspace Access
@app.route('/workspace/<int:workspace_id>')
@login_required
def workspace(workspace_id):
    # Looking for a workspace that matches the passed id
    workspace = Workspace.query.get_or_404(workspace_id)

    # Checking the users access
    if not WorkspaceMember.query.filter_by(user_id=current_user.id, workspace_id=workspace_id).first():
        return jsonify({"message:": "Acesso negado"}), 403

    # Getting boards and members from the workspace
    boards = Board.query.filter_by(workspace_id=workspace_id)
    members = User.query.join(WorkspaceMember).filter(WorkspaceMember.workspace_id == workspace_id).all()

    return render_template('workspace.html',
                                            workspace=workspace,
                                            boards=boards,
                                            members=members)

# Board Creation Route
@app.route('/create_board/<int:workspace_id>', methods=['POST'])
@login_required
def create_board(workspace_id):
    # Looking for a workspace that matches the passed id
    workspace = Workspace.query.get_or_404(workspace_id)

    # Checking the users access
    if not WorkspaceMember.query.filter_by(user_id=current_user.id, workspace_id=workspace_id).first():
        return jsonify({"message:": "Acesso negado"}), 403

    if request.is_json:
        data = request.get_json()
        title = data['title']
        about = data['about']

    else:
        title = request.form['title']
        about = request.form['about']

    if title == None:
        return jsonify({"message:": "É obrigatório informar um título."}), 400

    # Adding the board
    board = Board(title=title, about=about, workspace_id=workspace_id)
    db.session.add(board)
    db.session.commit()

    # Adding the default columns
    default_columns = ['To Do', 'Doing', 'Done']

    """for i, column_name in enumerate(default_columns):
        column = Column(title=column_name, board_id=board.id, position=i)
        db.session.add(column)"""

    for i in range(len(default_columns)):
        column = Column(title=default_columns[i], board_id =board.id, position=i)
        db.session.add(column)

    db.session.commit()

    # Returning to the endpoint that shows the workspaces
    return redirect(url_for('workspace', workspace_id=workspace_id))

# Board Access
@app.route('/board/<int:workspace_id>/<int:board_id>')
@login_required
def board(workspace_id, board_id):
    # Looking for a workspace that matches the passed id
    workspace = Workspace.query.get_or_404(workspace_id)
    board = Board.query.get_or_404(board_id)

    # Checking the users access
    if not WorkspaceMember.query.filter_by(user_id=current_user.id, workspace_id=workspace_id).first():
        return jsonify({"message:": "Acesso negado"}), 403

    # Getting columns from the workspace
    columns = Column.query.filter_by(board_id=board_id)

    return render_template('board.html',
                                            workspace=workspace,
                                            board=board,
                                            columns=columns)

# Card Creation Route
@app.route('/create_card/<int:workspace_id>/<int:board_id>', methods=['GET', 'POST'])
@login_required
def create_card(workspace_id, board_id):
    workspace = Workspace.query.filter_by(id=workspace_id).first()
    board = Board.query.filter_by(id=board_id, workspace_id=workspace_id).first()
    columns = Column.query.filter_by(board_id=board_id).all()

    if not workspace or not board:
        return jsonify({"message:": "Informações inexistentes."}), 404

    # Always compares the method type
    if request.method == 'POST':
        if request.is_json:
            data = request.json
            title = data['title']
            description = data['description']
            board_id = board.id
            column_id = 0
            responsible_id = data['responsible_id']
            deadline = datetime.strptime('2025-10-30 08:00:00', '%Y-%m-%d %H:%M:%S')

        else:
            title = request.form['title']
            description = request.form['description']
            board_id = board.id
            column_id = 0
            responsible_id = request.form['responsible_id']
            deadline = datetime.strptime('2025-10-30 08:00:00', '%Y-%m-%d %H:%M%:%S')

        if title == None:
            return jsonify({"message:": "É obrigatório informar um título."}), 400

        # Adding the card
        card = Card(title=title, description=description, board_id=board_id, column_id=column_id, responsible_id=responsible_id, deadline=deadline)
        db.session.add(card)
        db.session.commit()

        return jsonify({'message:': 'Card criado com sucesso!'}), 200

    return render_template('board.html',
                           columns=columns)

# Workspaces Listing Route
@app.route('/workspace_list')
@login_required
def workspace_list():
    # Searching for workspaces owned by the current user
    workspaces_one = Workspace.query.filter_by(owner_id=current_user.id).all()
    # Searching for workspaces that the current user is a member of.
    workspaces_two = Workspace.query.join(WorkspaceMember).filter(WorkspaceMember.user_id == current_user.id).all()

    # Merging both queries
    workspaces = list(set(workspaces_one + workspaces_two))

    workspaces_list = []

    # Creating a list to organize the data
    for wkspace in workspaces:
        workspaces_list.append({
            'id': wkspace.id,
            'title': wkspace.title,
            'description': wkspace.description,
            'owner_id': wkspace.owner_id,
            'created_date': wkspace.created_date
        })

    return jsonify(workspaces_list)

# Boards Listing Route
@app.route('/boards_list/<int:workspace_id>')
@login_required
def boards_list(workspace_id):
    # Looking for all boards that matches to the passed workspace id
    boards = Board.query.filter_by(workspace_id=workspace_id).all()

    # Checking the users access
    if not WorkspaceMember.query.filter_by(user_id=current_user.id, workspace_id=workspace_id).first():
        return jsonify({"message:": "Acesso negado"}), 403

    boards_list = []

    # Creating a list to organize the data
    for board in boards:
        boards_list.append({
            'id': board.id,
            'title': board.title,
            'about': board.about,
            'workspace_id': board.workspace_id,
            'created_date': board.created_date
        })

    return jsonify(boards_list)


# Card Listing Route
@app.route('/cards_list/<int:workspace_id>/<int:board_id>/')
@login_required
def cards_list(workspace_id, board_id):
    # Looking for all boards that matches to the passed workspace id
    cards = Card.query.filter_by(board_id=board_id).all()

    # Checking the users access
    if not WorkspaceMember.query.filter_by(user_id=current_user.id, workspace_id=workspace_id).first():
        return jsonify({"message:": "Acesso negado"}), 403

    cards_list = []

    # Creating a list to organize the data
    for card in cards:
        cards_list.append({
            'id': card.id,
            'title': card.title,
            'description': card.description,
            'board_id': card.board_id,
            'position': card.position,
            'column_id': card.column_id,
            'responsible_id': card.responsible_id,
            'created_date': card.created_date,
            'deadline': card.deadline
        })

    return jsonify(cards_list)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
