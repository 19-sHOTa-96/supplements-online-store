from flask import Flask, render_template
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager, current_user
from flask_admin import Admin


mail = Mail()
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'user.login'
administration = Admin(name='Brossupp', template_mode='bootstrap3')

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	mail.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)
	administration.init_app(app)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .user import user as user_blueprint
	app.register_blueprint(user_blueprint, url_prefix='/user')

	from .blog import blog as blog_blueprint
	app.register_blueprint(blog_blueprint, url_prefix='/blog')

	from .admin import admin_panel as admin_blueprint
	app.register_blueprint(admin_blueprint)

	return app


	@main.app_context_processor
	def inject_permission():
		return dict(Permission=Permission)

