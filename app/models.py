from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


## Database configuration
class Product(db.Model):
	__tablename__ = 'products'
	id = db.Column(db.Integer, primary_key=True)
	product_name = db.Column(db.String(64))
	image = db.Column(db.String(64))
	price = db.Column(db.String(64))

	def __str__(self):
		return self.product_name


class User(UserMixin, db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(64))
	last_name = db.Column(db.String(64))
	email = db.Column(db.String(64), unique=True)
	phone = db.Column(db.String(64), unique=True)
	password = db.Column(db.String(300))
	password_hash = db.Column(db.String(200))
	confirmed = db.Column(db.Boolean, default=False)

	@property
	def password(self):
		raise AttributeError('password is not readable')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)		

	def generate_confirmation_token(self, expiration=3600):
		s = Serializer(current_app.config['SECRET_KEY'], expiration)
		return s.dumps({'confirm': self.id}).decode('utf-8')	

	def confirm(self, token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			data = s.loads(token.encode('utf-8'))
		except:
			return False
		if data.get('confirm') != self.id:
			return False
		self.confirmed = True
		db.session.add(self)
		return True				

	def __str__(self):
		return self.first_name


				