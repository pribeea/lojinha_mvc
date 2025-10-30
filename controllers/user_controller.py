from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models import get_db
from models.user import User

user_bp = Blueprint('user_controller', __name__, template_folder='../templates/users')

@user_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@user_bp.route('/users')
@login_required
def list_users():
    db = get_db()
    users = db.query(User).all()
    db.close()
    return render_template('users_list.html', users=users)
