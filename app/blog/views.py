from flask import render_template
from . import blog


@blog.route('/post')
def post():
	return render_template('blog/post.html')

