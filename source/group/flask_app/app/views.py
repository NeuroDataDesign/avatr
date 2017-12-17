from flask import render_template, request
from app import app
from forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route("/pull_tif", methods=["GET", "POST"])
def pull_tif():
	form = LoginForm(request.form)
	if request.method == 'POST' and form.validate():
		flash('worked')
	#	message1 = request.form['channel']
	#if message1:
	#	print(message1)
	return render_template("login.html", title='Sign In', form=form)

@app.route("/push_tif", methods=["GET", "POST"])
def push_tif():
	form = LoginForm(request.form)
	if request.method == 'POST' and form.validate():
		flash('worked')
	#	message1 = request.form['channel']
	#if message1:
	#	print(message1)
	return render_template("login.html", title='Sign In', form=form)

