from . import main
from flask import Flask, render_template, redirect, url_for, flash, session, current_app
from .. import db
from ..models import User, Product
from ..email import send_contact_mail
from .forms import ContactForms

## App Routes
@main.route('/')
def home():
	return render_template('home.html')

	
@main.route('/products')
def products():
	products = Product.query.all()
	return render_template('products.html', products=products)


@main.route('/contact', methods=['GET', 'POST'])
def contact():
	form = ContactForms()
	if form.validate_on_submit():
		mail_sender_info = {}	
		mail_sender_info['first_name'] = form.first_name.data
		mail_sender_info['email'] = form.email.data
		mail_sender_info['phone'] = form.phone.data
		mail_sender_info['message'] = form.message.data

		send_mail(app.config['RECIPIENT_MAIL'], app.config['MAIL_SUBJECT_PREFIX'], 
				  'mail/mail-contact.html', mail_sender_info=mail_sender_info)

	return render_template('contact.html', form=form)	

@main.route('/about')
def about():
	return render_template('about.html')
	


	