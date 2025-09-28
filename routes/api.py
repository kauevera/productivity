from flask import render_template, request, redirect, url_for, jsonify, Blueprint
from flask_login import login_required, current_user
from models import db, Workspace, WorkspaceMember, Board, Column, Card
from datetime import datetime

api_bp = Blueprint("api", __name__)

# Workspace Creation Route
@api_bp.route('/create_workspace', methods=['GET', 'POST'])
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

        return redirect(url_for('views.index'))
        ##return jsonify({"message:": "Workspace criado com sucesso."}), 200

    return render_template('home.html',
                           workspaces=workspaces)



# Board Creation Route
@api_bp.route('/create_board/<int:workspace_id>', methods=['POST'])
@login_required
def create_board(workspace_id):
    # Looking for a workspace that matches the passed id
    workspace = Workspace.query.get_or_404(workspace_id)

    # Checking the users access
    if not WorkspaceMember.query.filter_by(user_id=current_user.id, workspace_id=workspace.id).first():
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

    # Returning to the endpoint that shows the boards
    return redirect(url_for('views.workspace', workspace_id=workspace.id)), 200



# Card Creation Route
@api_bp.route('/create_card', methods=['POST'])
@login_required
def create_card():
    if request.is_json:
        data = request.json
        column_id = data['column_id']
        title = data['title']
        description = data['description']
        responsible_id = data['responsible_id']
        deadline = datetime.strptime(data['deadline'], '%Y-%m-%dT%H:%M:%S')

    else:
        column_id = request.form['column_id']
        title = request.form['title']
        description = request.form['description']
        responsible_id = request.form['responsible_id']
        deadline = datetime.strptime(data['deadline'], '%Y-%m-%dT%H:%M%:%S')

    if title == None:
        return jsonify({"message:": "É obrigatório informar um título."}), 400
    
    # Getting the board_id
    column = Column.query.filter_by(id=column_id).first()
    board_id = column.board_id
    # Getting the board
    board = Board.query.filter_by(id=board_id).first()

    # Adding the card
    card = Card(column_id=column_id, title=title, description=description, board_id=board_id, responsible_id=responsible_id, deadline=deadline)
    db.session.add(card)
    db.session.commit()

    # Returning to the endpoint that shows the cards
    return redirect(url_for('views.board', board_id=board.id)), 200

# Card Deleting Route
@api_bp.route('/delete_card/<int:card_id>', methods=['DELETE'])
@login_required
def delete_card(card_id):
    # Checking the card existence
    card = Card.query.filter_by(id=card_id).first()
    if not card:
        return jsonify({"message:": "O elemento informado não existe"}), 404

    # Getting the board_id
    board_id = card.board_id
    # Getting the board
    board = Board.query.filter_by(id=board_id).first()
    # Getting the workspace_id
    workspace_id = board.workspace_id
    # Getting the workspace
    workspace = Workspace.query.filter_by(id=workspace_id).first()

    # Checking the users access
    if not WorkspaceMember.query.filter_by(user_id=current_user.id, workspace_id=workspace.id).first():
        return jsonify({"message:": "Acesso negado"}), 403

    # Removing the card
    db.session.delete(card)
    db.session.commit()

    # Returning to the endpoint that shows the cards
    return redirect(url_for('views.board', board_id=board.id)), 200