from wtforms import form, fields, validators
from werkzeug.security import generate_password_hash, check_password_hash


class LoginForm(form.Form):
	login = fields.StringField(validators=[validators.InputRequired()])
	password = fields.StringField(validators=[validators.InputRequired()])

	def validate_login(self, field):
		user = self.get_user()

		if user is None:
			raise validators.ValidationError('Invalid user')

		if not check_password_hash(user.password, self.password.data):
			raise validators.ValidationError('Invalid password')

	def get_user(self):
		return db.session.query(User).filter_by(login=self.login.data).first()	


class RegistrationForm(form.Form):
	login = fields.StringField(validators=[validators.InputRequired()])
	email = fields.StringField(validators=[validators.InputRequired()])
	password = fields.PasswordField(validators=[validators.InputRequired()])

	def validate_login(self, field):
		if db.session.query(User).filter_by(login=self.login.data).count() > 0:
			raise validators.ValidationError('Duplicate username')

							