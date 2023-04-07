import os
from app import create_app, db
from app.models import User, Role, Comment, Profile, Wishlist, Product, ProductBrand, ProductType, ProductDetail, Permission
from flask_migrate import Migrate

app = create_app(os.getenv('CONFIG') or 'default')
migrate = Migrate(app, db)


@app.shell_context_processor
def shell_context():
	return dict(
				db=db, User=User, Role=Role, Wishlist=Wishlist, Comment=Comment, 
				Product=Product, ProductBrand=ProductBrand, ProductType=ProductType,
				ProductDetail=ProductDetail, Permission=Permission
				)
	
if __name__ == "__main__":
	app.run(debug=True)

		