from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import get_db
from models.product import Product

product_bp = Blueprint('product_controller', __name__, template_folder='../templates/products')

@product_bp.route('/')
@product_bp.route('/products')
def list_products():
    if not current_user.is_authenticated:
        return render_template('index.html')
    
    db = get_db()
    products = db.query(Product).filter_by(user_id=current_user.id).all()
    db.close()
    return render_template('list.html', products=products)

@product_bp.route('/products/create', methods=['GET', 'POST'])
@login_required
def create_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = request.form.get('price')
        
        db = get_db()
        product = Product(
            name=name, 
            description=description, 
            price=float(price), 
            user_id=current_user.id
        )
        
        db.add(product)
        db.commit()
        db.close()
        
        flash('Produto criado com sucesso!')
        return redirect(url_for('product_controller.list_products'))
    
    return render_template('create.html')

@product_bp.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    db = get_db()
    product = db.query(Product).filter_by(id=product_id).first()
    
    if not product:
        flash('Produto não encontrado.')
        db.close()
        return redirect(url_for('product_controller.list_products'))
    
    if product.user_id != current_user.id:
        flash('Você não tem permissão para editar este produto.')
        db.close()
        return redirect(url_for('product_controller.list_products'))
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        
        db.commit()
        db.close()
        
        flash('Produto atualizado com sucesso!')
        return redirect(url_for('product_controller.list_products'))
    
    db.close()
    return render_template('edit.html', product=product)

@product_bp.route('/products/<int:product_id>/delete')
@login_required
def delete_product(product_id):
    db = get_db()
    product = db.query(Product).filter_by(id=product_id).first()
    
    if not product:
        flash('Produto não encontrado.')
        db.close()
        return redirect(url_for('product_controller.list_products'))
    
    if product.user_id != current_user.id:
        flash('Você não tem permissão para excluir este produto.')
        db.close()
        return redirect(url_for('product_controller.list_products'))
    
    db.delete(product)
    db.commit()
    db.close()
    
    flash('Produto excluído com sucesso!')
    return redirect(url_for('product_controller.list_products'))
