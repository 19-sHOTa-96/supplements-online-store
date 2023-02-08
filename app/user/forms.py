from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo


## Form Configuration
class RegistrationForms(FlaskForm):
	first_name = StringField('First name', validators=[DataRequired()])
	last_name = StringField('Last name', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired(), Email()])
	phone = StringField('Last name', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired(),
		EqualTo('password_2', message='Password must match.')])
	password_2 = PasswordField('Confirm Password', validators=[DataRequired()])
	submit = SubmitField('Submit', validators=[DataRequired()])

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValueError('Email already registered.')

	def validate_username(self, field):
		if User.query.filter_by(username=field.data).first():
			raise ValidationError('Username already in user.')	


class LoginForms(FlaskForm):
	first_name = StringField('First name', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	stay_logged = BooleanField('stay logged in')
	submit = SubmitField('Submit')


class ContactForms(FlaskForm):
	first_name = StringField('First name', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	phone = StringField('Phobe', validators=[DataRequired()])
	message = TextAreaField('Send Message...', validators=[DataRequired()])
	submit = SubmitField('Submit')

	