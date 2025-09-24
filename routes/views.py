from flask import render_template, jsonify, Blueprint
from flask_login import login_required, current_user
from models import User, Workspace, WorkspaceMember, Board, Column

views_bp = Blueprint("views", __name__)

# Base Route
@views_bp.route('/index')
@login_required
def index():
    # Looking for all workspaces that the user is member of.
    workspaces = Workspace.query.join(WorkspaceMember).filter(WorkspaceMember.user_id == current_user.id).all()

    return render_template('home.html',
                           workspaces=workspaces)

# Workspace Access
@views_bp.route('/workspace/<int:workspace_id>')
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

# Board Access
@views_bp.route('/board/<int:board_id>')
@login_required
def board(board_id):
    # Looking for a workspace that matches the passed id
    board = Board.query.get_or_404(board_id)
    workspace = Workspace.query.filter_by(id=board.workspace_id).first()
    workspace_id = workspace.id
    workspace_member = WorkspaceMember.query.filter_by(workspace_id=workspace_id).first()

    # Checking the users access
    if not WorkspaceMember.query.filter_by(user_id=current_user.id, workspace_id=workspace.id).first():
        return jsonify({"message:": "Acesso negado"}), 403

    # Getting columns from the workspace
    columns = Column.query.filter_by(board_id=board_id).order_by(Column.position).all()

    cards = {
        'columns': [
            {
                'id': col.id,
                'name': col.title,
                'cards': [
                    {
                        'id': card.id,
                        'title': card.title,
                        'description': card.description,
                        'assigned_to': card.responsible_id,
                        'position': card.position
                    }
                    for card in col.cards
                ]
            }
            for col in columns
        ]
    }

    return render_template('board.html',
                           board=board,
                           columns=columns,
                           cards=cards,
                           workspace_member=workspace_member)