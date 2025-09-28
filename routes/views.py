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

# Listing users
@views_bp.route('/listing_users')
@login_required
def listing_users():
    # Searching for all users
    users = User.query.all()

    users_matriz = []

    for user in users: 
        users_matriz.append(
            {
                "id" : user.id,
                "username" : user.username,
                "nickname" : user.nickname,
                "email" : user.email,
                "gender" : user.gender,
                "age" : user.age,
            }
        )

    return jsonify(users_matriz), 200

# Listing workspace members
@views_bp.route('/listing_workspace_members/<int:board_id>')
@login_required
def listing_workspace_members(board_id):
    # Looking for a workspace that matches the passed id
    board = Board.query.get_or_404(board_id)
    workspace = Workspace.query.filter_by(id=board.workspace_id).first()
    workspace_id = workspace.id

    # Checking the user access
    if not WorkspaceMember.query.filter_by(user_id=current_user.id, workspace_id=workspace.id).first():
        return jsonify({"message:": "Acesso negado"}), 403
    
    # Searching for all workspace members
    workspace_members = WorkspaceMember.query.filter_by(workspace_id=workspace_id).all()

    workspace_matriz = []

    for member in workspace_members: 
        workspace_matriz.append(
            {
                "member_id" : member.id,
                "user_id" : member.user_id,
                "username" : member.user.username,
                "nickname" : member.user.nickname,
                "email" : member.user.email,
                "gender" : member.user.gender,
                "age" : member.user.age,
                "role" : member.role,
                "workspace_title" : member.workspace.title
            }
        )

    return jsonify(workspace_matriz), 200

