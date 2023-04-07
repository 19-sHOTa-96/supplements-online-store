from . import main
from flask import render_template, redirect, url_for, flash, session, current_app, request
from .. import db
from ..models import User, Product, ProductDetail, ProductType, ProductReview
from ..email import send_contact_mail
from .forms import ContactForms, ReviewtForm
from flask_login import current_user

## App Routes
@main.route('/')
def home():
	return render_template('home.html')

	
@main.route('/products/<product_type>')
def products(product_type):
	# products = Product.query.all()
	product_type = ProductType.query.filter_by(product_type=product_type).first()
	products = Product.query.filter_by(product_type_id=product_type.id).all()
	return render_template('products.html', products=products)


@main.route('/product_details/<product_id>', methods=['GET', 'POST'])
def product_details(product_id):
	form = ReviewtForm()
	productdetails = ProductDetail.query.get(product_id)
	product = Product.query.get(productdetails.product_product_detail.id)
	product_review = ProductReview.query.filter_by(product_review_id=product.id).all()
	print(product_review)

	# product_product_detail
	if form.validate_on_submit():
		product_review = ProductReview(review=form.review.data, author=current_user.first_name, product_review=product)
		db.session.add(product_review)
		db.session.commit()

		return redirect(url_for('main.product_details', product_id=product_id))

	return render_template('product_details.html', productdetails=productdetails, product_id=product_id, product_review=product_review, form=form)


@main.route('/contact', methods=['GET', 'POST'])
def contact():
	form = ContactForms()
	if form.validate_on_submit():
		mail_sender_info = {}	
		mail_sender_info['first_name'] = form.first_name.data
		mail_sender_info['email'] = form.email.data
		mail_sender_info['phone'] = form.phone.data
		mail_sender_info['message'] = form.message.data

		send_contact_mail(current_app.config['RECIPIENT_MAIL'], current_app.config['MAIL_SUBJECT_PREFIX'],
						  'mail/mail-contact', current_app.config['MAIL_USERNAME'], mail_sender_info=mail_sender_info)

	return render_template('contact.html', form=form)	


@main.route('/about')
def about():
	return render_template('about.html')
	

@main.route('/blog')
def blog():
	return render_template('blog.html')


@main.route('/review')
def review():
	return render_template('review.html')

