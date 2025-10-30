from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import get_db
from models.user import User

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('product_controller.list_products'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        db = get_db()
        
        if db.query(User).filter_by(email=email).first():
            flash('Email já cadastrado.')
            db.close()
            return render_template('register.html')
        
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.add(user)
        db.commit()
        db.close()
        
        flash('Registro realizado com sucesso! Faça login.')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('product_controller.list_products'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        db = get_db()
        user = db.query(User).filter_by(email=email).first()
        db.close()
        
        if user and user.verify_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('product_controller.list_products'))
        else:
            flash('Email ou senha inválidos.')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você saiu da sua conta.')
    return redirect(url_for('auth.login'))
