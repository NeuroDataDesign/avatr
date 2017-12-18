from flask import render_template, request
from app import app

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route("/pull_tif", methods=["GET", "POST"])
def pull_tif():
	## TODO:should do some form validation here but w/e for now
	col = request.form["collection"]
	exp = request.form["experiment"]
	return "col" + "exp"

@app.route("/push_tif", methods=["GET", "POST"])
def push_tif():
	#	message1 = request.form['channel']
	#if message1:
	#	print(message1)
	return "Good shit"
