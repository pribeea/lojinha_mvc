from flask_login import LoginManager
from models import get_db
from models.user import User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    user = db.query(User).get(int(user_id))
    db.close()
    return user
