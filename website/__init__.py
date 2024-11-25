import os
from flask_migrate import Migrate
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'GERM'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/library_management'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Set the directory for storing uploaded PDF files
    app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'uploads')
    app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

    # Ensure the upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    db.init_app(app)

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)

    from .models import Book

    # Register blueprints
    from .admin_views import admin
    from .user_views import user

    app.register_blueprint(user, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')

    return app
