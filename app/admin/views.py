from . import admin_panel
from ..models import Product, ProductDetail, ProductReview, ProductBrand, ProductType
from werkzeug.security import generate_password_hash, check_password_hash
from flask_admin.contrib.sqla import ModelView 
from flask_admin.form import FileUploadField
from flask_admin import BaseView, expose
from flask_admin.form import BaseForm
from flask_admin.contrib import sqla
from flask_login import current_user
from .forms import RegistrationForm
from .. import administration
from flask_admin import Admin
import flask_admin as admin
import os.path as op
from .. import db
from flask import abort


class BrosSuppView(ModelView):
	can_delete = True
	page_size = 50
	can_export = True

	def is_accessible(self):
		if str(current_user.role) == 'administrator':
			return True
		abort(404)

class UserView(ModelView):
	can_delete = False
		
class AnalyticsView(BaseView):
	@expose('/')
	def index(self):
		return self.render('admin/analytics_index.html')

class StatisticsView(BaseView):
	@expose('/')
	def index(self):
		return self.render('admin/statistics_index.html')

def prefix_name(obj, file_data):
    parts = op.splitext(file_data.filename)
    return secure_filename('file-%s%s' % parts)

class MyForm(BaseForm):
    upload = FileUploadField('File', namegen=prefix_name)


#----------------------------------------------------------------------|



#----------------------------------------------------------------------|


administration.add_view(BrosSuppView(Product, db.session))
administration.add_view(BrosSuppView(ProductBrand, db.session))
administration.add_view(BrosSuppView(ProductType, db.session))
administration.add_view(BrosSuppView(ProductDetail, db.session))
administration.add_view(BrosSuppView(ProductReview, db.session))

administration.add_view(AnalyticsView(name='Analytics', endpoint='analytics'))
administration.add_view(StatisticsView(name='Statistics', endpoint='statistics'))
