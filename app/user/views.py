from . import user
from flask import render_template, redirect, url_for, flash, session, request
from flask_login import login_required, login_user, logout_user, current_user
from ..models import User
from .forms import RegistrationForms, LoginForms, ContactForms
from .. import db

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

			token = user.generate_confirmation_token()
			send_confirmation_mail(user.email, 'Confirm Your Account',
				'user/email/mail-confirmation', user=user, token=token)

			flash('A confirmation email has been sent to you by email.')

			return redirect(url_for('main.home'))		

	return render_template('user/registration.html', form=form)


@user.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		db.session.commit()
		flash('You have confirmed your account. Thanks!')
	else:
		flash('The confirmation link is invalid or has expired.')		
	return redirect(url_for('main.index'))	


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
	send_email(current_user.email, 'Confirm Your Account',
		'user/email/mail-confirmation', user=user, token=token)

	flash('A new confirmation email has been sent to you by email.')
	return redirect(url_for('main.home'))


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


	