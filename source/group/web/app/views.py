from app import app
from flask import jsonify
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/pull_stack', methods=['GET'])
def pull_stack():
	return 'hi'
