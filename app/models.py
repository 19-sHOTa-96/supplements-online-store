from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


## USERS MODEL
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))


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

	# Relationships
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
	comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
	profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
	wishlist_id = db.Column(db.Integer, db.ForeignKey('wishlists.id'))
	# review_id = db.Column(db.Integer, db.ForeignKey('productreviews.id'))

	def __init__(self, **kwargs):
		super(User, self).__init__(**kwargs)
		if self.role is None:
			if self.email == current_app.config['BROSSUPP_EMAIL']:
				self.role = Role.query.filter_by(name='Administrator').first()
			if self.role is None:
				self.role = Role.query.filter_by(default=True).first()	

	def can(self, perm):
		return self.role is not None and self.role.has_permission(perm)

	def is_administrator(self):
		return self.can(Permission.ADMIN)	

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

	def __repr__(self):
		return self.first_name


class Role(db.Model):
	__tablename__ = 'roles'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), unique=True)
	default = db.Column(db.Boolean, default=False, index=True)
	permissions = db.Column(db.Integer)
	user_role = db.relationship('User', backref='role', lazy='dynamic')

	def __init__(self, **kwargs):
		super(Role, self).__init__(**kwargs)
		if self.permissions is None:
			self.permissions = 0

	def add_permission(self, perm):
		if not self.has_permission(perm):
			self.permissions += perm

	def remove_permission(self, perm):
		if self.has_permission(perm):
			self.permissions -= perm

	def reset_permission(self):
		self.permissions = 0

	def has_permission(self, perm):
		return self.permissions & perm == perm							

	@staticmethod
	def insert_roles():
		roles = {
			'User': [],
			'Moderator': [],
			'Administrator': []
		}	

		default_role = 'User'
		for r in roles:
			role = Role.query.filter_by(name=r).first()
			if role is None:
				role = Role(name=r)
			role.reset_permission()
			for perm in roles[r]:
				role.add_permission(perm)
			role.default = (role.name == default_role)		

			db.session.add()
		db.session.commit()	

	def __repr__(self):
		return self.name


class AnonymousUser(AnonymousUserMixin):
	def can(self, permissions):
		return False

	def is_administrator(self):
		return False	


class Permission:
	LIKE = 1
	REVIEW = 2
	WRITE = 4
	MODERATE = 8
	ADMIN = 16


class Profile(db.Model):
	__tablename__ = 'profiles'

	id = db.Column(db.Integer, primary_key=True)
	nick_name = db.Column(db.String(64), unique=True, nullable=True)
	city = db.Column(db.String(64), nullable=True)
	image = None

	user_profile = db.relationship('User', backref='profile', uselist=False)

	def __repr__(self):
		return self.nick_name


class Wishlist(db.Model):
	__tablename__ = 'wishlists'

	id = db.Column(db.Integer, primary_key=True)
	user_wishlist = db.relationship('User', backref='wishlist')

	def __repr__(self):
		return self.user_wishlist


class Comment(db.Model):
	__tablename__ = 'comments'

	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(500), nullable=True)
	user_comment = db.relationship('User', backref='comment')

	def __repr__(self):
		return self.body


## PRODUCT MODELS
class Product(db.Model):
	__tablename__ = 'products'

	id = db.Column(db.Integer, primary_key=True)
	product_name = db.Column(db.String(64))
	image = db.Column(db.String(64))
	price = db.Column(db.String(64))

	# Relationships
	product_detail_id = db.Column(db.Integer, db.ForeignKey('productdetails.id'))
	product_brand_id = db.Column(db.Integer, db.ForeignKey('productbrands.id'))
	product_type_id = db.Column(db.Integer, db.ForeignKey('producttypes.id'))

	# Relationships
	product_product_review = db.relationship('ProductReview', backref='product_review')

	def __repr__(self):
		return self.product_name


class ProductDetail(db.Model):
	__tablename__ = 'productdetails'

	id = db.Column(db.Integer, primary_key=True)
	product_name = db.Column(db.String(64))
	product_description = db.Column(db.String(500))
	product_review = db.Column(db.String(500))
	product_product_detail = db.relationship('Product', uselist=False, backref='product_detail')

	def __repr__(self):
		return self.product_name


class ProductType(db.Model):
	__tablename__ = 'producttypes'

	id = db.Column(db.Integer, primary_key=True)
	product_type = db.Column(db.String(64))
	product_product_type = db.relationship('Product', backref='product_type')

	def __repr__(self):
		return self.product_type


class ProductBrand(db.Model):
	__tablename__ = 'productbrands'

	id = db.Column(db.Integer, primary_key=True)
	product_brand = db.Column(db.String(64))
	product_product_brand = db.relationship('Product', backref='product_brand')

	def __repr__(self):
		return self.product_brand


class ProductReview(db.Model):
	__tablename__ = 'productreviews'

	id = db.Column(db.Integer, primary_key=True)
	review = db.Column(db.String(500))
	author = db.Column(db.String(64), nullable=True)
	product_review_id = db.Column(db.Integer, db.ForeignKey('products.id'))
	# user_review = db.relationship('User', backref='user_review')

	def __repr__(self):
		return self.review



## ADMIN MODELS
# class Admin(db.Model):
# 	__tablename__ = 'admins'

# 	id = db.Column(db.Integer, primary_key=True)
# 	username = db.Column(db.String(64))
# 	email = db.Column(db.String(64))
# 	password_hash = db.Column(db.String(200))
# 	password = db.Column(db.String(64))

# 	@property
# 	def password(self):
# 		raise('password is not readable')

# 	@password.setter
# 	def password(self, password):
# 		self.password_hash = generate_password_hash(password)	

# 	def check_password(self, password):
# 		return check_password_hash(self.password_hash, password)

# 	@property
# 	def is_autheticated(self):
# 		return True

# 	@property
# 	def is_active(self):
# 		return True

# 	@property
# 	def is_anonymous(self):
# 		return False

# 	def get_id(self):
# 		return self.id

# 	def __unicode__(self):
# 		return self.username			

# 	def __repr__(self):
# 		return self.first_name	

	