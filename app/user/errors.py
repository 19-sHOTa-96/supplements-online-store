from . import user
from flask import render_template

@user.app_errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@user.app_errorhandler(500)
def internal_server_error(e):
	return render_template('505.html'), 500

