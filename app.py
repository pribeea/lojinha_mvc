from flask import Flask, render_template
from config import Config
from auth.utils import login_manager
from auth.routes import auth_bp
from controllers.user_controller import user_bp
from controllers.product_controller import product_bp
from models import create_tables

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    login_manager.init_app(app)
    
    create_tables()
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(product_bp)

    @app.route('/')
    def index():
        render_template('index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
