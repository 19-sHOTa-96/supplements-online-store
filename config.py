import os
basedir = os.path.abspath(os.path.dirname(__file__))

# 'mysql+pymysql://root:Pass2500-9!@localhost/suppdb'

class Config:
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'temporary secret key'
	MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.googlemail.com')
	MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in \
		['true', 'on', '1']
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	RECIPIENT_MAIL = os.environ.get('RECIPIENT_MAIL')
	MAIL_SUBJECT_PREFIX = '[SupplementStore]'
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
	'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
	TESTING = True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
	'sqlite:///'

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
	'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
	'development': DevelopmentConfig,
	'testing': TestingConfig,
	'production': ProductionConfig,
	'default': DevelopmentConfig
}					
