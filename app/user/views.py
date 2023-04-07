from . import user
from flask import render_template, redirect, url_for, flash, session, request, current_app
from flask_login import login_required, login_user, logout_user, current_user
from ..models import User

from .forms import RegistrationForms, LoginForms, ContactForms, ChangePasswordForms, ChangeEmailForms, \
				   ResetPassCodeForms, ConfirmPassCodeForms, ResetPasswordForms
				   
from .. import db
from ..email import send_confirmation_email, send_contact_mail
from ..utility.helper import generate_code
from ..utility.decorators import permission_required, admin_required


## Registration And Confiramtion Block 
@user.route('/registration', methods=['GET', 'POST'])
def registration():
	form = RegistrationForms()
	user = User.query.filter_by(first_name=form.first_name.data).first()

	if user is None:
		first_name, last_name = form.first_name.data, form.last_name.data
		email, phone = form.email.data, form.phone.data
		password = form.password.data

		if all((first_name, last_name, email, phone, password)):
			new_user = User(first_name=first_name, last_name=last_name,
							email=email, phone=phone, password=password)

			db.session.add(new_user)
			db.session.commit()

			token = new_user.generate_confirmation_token()
			
			login_user(new_user) 

			send_confirmation_email(new_user.email, 'Confirm Your Account',
				'mail/mail-confirmation', user=new_user, token=token)

			flash('A confirmation email has been sent to you by email.')

			return redirect(url_for('main.home'))		

	return render_template('user/registration.html', form=form)


@user.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.home'))
	if current_user.confirm(token):
		db.session.commit()
		flash('You have confirmed your account. Thanks!')
	else:
		flash('The confirmation link is invalid or has expired.')		
	return redirect(url_for('main.home'))	


@user.before_app_request
def before_request():
	if current_user.is_authenticated \
		and not current_user.confirmed \
		and request.blueprint != 'user' \
		and request.endpoint != 'static':
		return redirect(url_for('user.uncorfirmed'))
		

@user.route('/uncorfirmed')
def uncorfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.home'))
	return render_template('user/uncorfirmed.html')				


@user.route('/confirm')
@login_required
def resend_confirmation():
	token = current_user.generate_confirmation_token()
	send_confirmation_email(current_user.email, 'Confirm Your Account',
		'user/email/mail-confirmation', user=user, token=token)

	flash('A new confirmation email has been sent to you by email.')
	return redirect(url_for('user.home'))


@user.route('/reset_password_code', methods=['GET', 'POST'])
def reset_password_code():
	form = ResetPassCodeForms()
	code = generate_code(6)
	user = User.query.filter_by(email=form.email.data).first()

	if form.validate_on_submit():
		print(current_app.config['MAIL_USERNAME'], user.email, code)
		send_contact_mail(form.email.data, 'Password reset',
					      'mail/reset_password', current_app.config['MAIL_USERNAME'], user=user, code=code)

		return redirect(url_for('user.confirm_reset_password_code', user_id=user.id, confirm_code=code))
		flash('Code is incorrect.')		

	return render_template('user/reset_password_code.html', form=form)


@user.route('/confirm_reset_password_code/<user_id>/<confirm_code>', methods=['GET', 'POST'])
def confirm_reset_password_code(user_id, confirm_code):
	form = ConfirmPassCodeForms()
	print('CONFIRMATION CODE', confirm_code)

	if form.validate_on_submit():
		if form.confirm_code.data == confirm_code:
			return redirect(url_for('user.reset_password', user_id=user_id))
		return '<h1>Error...</h1>'	

	return render_template('user/confirm_reset_password_code.html', form=form, user_id=user_id, confirm_code=confirm_code)	


@user.route('/reset_password/<user_id>', methods=['GET', 'POST'])
def reset_password(user_id):
	user = User.query.get(user_id)
	form = ResetPasswordForms()

	if form.validate_on_submit():
		user.password = form.new_password.data
		db.session.commit()
		flash('Your password changed successfully')
		return redirect(url_for('main.home'))

	return render_template('user/reset_password.html', form=form, user_id=user_id)		


@user.route('/change_password')
def change_password():
	form = ChangePasswordForms()
	return render_template('user/change_password.html', form=form)


@user.route('/change_email')
def change_email():
	form = ChangeEmailForms()
	return render_template('user/change_email.html', form=form)
	

## Login Logout Block
@user.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForms()

	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()

		if not user is None:
			first_name, email = form.first_name.data, form.email.data
			user_password = form.password.data

			if user.first_name == first_name:
				if user.email == email:
					if user.check_password(user_password):
						login_user(user, form.stay_logged)
						return redirect(url_for('main.home'))
					else:
						flash('Password is icorrect.')
				else:
					flash('Email is icorrect.')
			else:
				flash('First name is icorrect.')					

	return render_template('user/login.html', form=form)	


@user.route('/logout')
def logout():
	logout_user()
	flash('You are successfully logged out.')
	return redirect(url_for('main.home'))


	