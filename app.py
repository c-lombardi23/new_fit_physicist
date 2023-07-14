from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager, login_user, logout_user
from flask import jsonify
from flask_mail import Mail, Message
from flask_migrate import Migrate
from werkzeug.utils import secure_filename, send_from_directory
from flask_sitemap import Sitemap
from models_forms import db
from routes.main_routes import main_bp
from routes.authenticate_routes import authenticate_bp
from routes.article_routes import article_bp
from models_forms import User
import psycopg2




app = Flask(__name__, static_url_path='/static')
app.register_blueprint(main_bp)
app.register_blueprint(authenticate_bp)
app.register_blueprint(article_bp)


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'clombar1@email.essex.edu'
app.config['MAIL_PASSWORD'] = 'lcjtpfdsfgygheqy'
app.config['SITEMAP_INCLUDE_RULE_WITHOUT_PARAMS'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_DEFAULT_SENDER'] = 'clombar1@email.essex.edu'

mail = Mail(app)
sitemap = Sitemap(app=app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'main.index'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

base_dir = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = os.path.join(app.root_path, 'static/uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


app.config["SQLALCHEMY_DATABASE_URI"] =  "postgresql://fit_physicist_database_user:1rADt20ms1EOrP8F3EfpymJwT7oIS4kx@dpg-cioqc5h5rnurl3u99chg-a:5432/fit_physicist_database"
app.config["SQLACLHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = 'you-will-never-guess1315123'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


db.init_app(app)
migrate = Migrate(app, db)

with app.app_context():
    db.create_all()

 
@sitemap.register_generator
def index_sitemap():
    return [
        ('index', {}),
        ('about', {}),
        ('contact', {}),
        ('article', {}),
        ('contribute', {}),
        ('cardio_article', {}),
        ('nutrition_advice', {})
    ]

@app.route('/sitemap.xml')
def sitemap():
    return sitemap.sitemap_xml()


if __name__ == '__main__':
    
    app.run(debug=False)
            
