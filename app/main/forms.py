from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email


## Form Configuration
class ContactForms(FlaskForm):
	first_name = StringField('First name', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	phone = StringField('Phobe', validators=[DataRequired()])
	message = TextAreaField('Send Message...', validators=[DataRequired()])
	submit = SubmitField('Submit')

	