##################################################################
#This is used to import clases from flask
from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from flask.ext.sqlalchemy import SQLAlchemy
from functools import wraps
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
#end of imports

####################################################################
#Apps 
app = Flask(__name__)
app.secret_key = "S2q3q3kbpy27"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)
from models import *
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
#end of apps

####################################################################
#Routes Begin
####################################################################

#login 
def login_required(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('You need to login as Admin.')
			return redirect(url_for('admin'))
	return wrap		
###################################################################

#logout
@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	flash('You have been logged out')
	return redirect(url_for('home'))
# end of login and logout routes

####################################################################
#pages routes
####################################################################

# dashboad
@app.route('/dashboard')
@login_required
def dashboard():
	users = db.session.query(User).order_by(User.name)
	return render_template("dashboard.html", users=users)
@app.route('/search')
@login_required
def search():
	users = db.session.query(User).filter_by(id)
	return render_template("search.html", users=users)

#########################################################################

#home page
@app.route('/', methods=['GET', 'POST']) 
def home():
	error = None
	if request.method == 'POST':
		name = request.form['name']
		phone_number = request.form['phone_number']
		email = request.form['email']
		address = request.form['address']
		table = request.form['table']
		user_reg = User(name,phone_number,email,address,table)
		db.session.add(user_reg)
		db.session.commit()
		flash('Registration Successfull.')
	return render_template('home.html',error = error)

############################################################################
#Admin login page
@app.route('/admin', methods=['GET', 'POST'])
def admin():
	error = None
	if  request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'myAdmin':
			error = 'Invalid login details, Please meet the Admin'
		else:
			session['logged_in'] = True
			flash('Login sucessfull')
			return redirect(url_for('dashboard'))
	return render_template('admin.html', error=error)

#############################################################################
#Error Handeling 
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

##############################################################################
#Edit Page
@app.route('/edit/<id>', methods=['POST', 'GET'])
@login_required
def edit (id):
    users = User.query.get(id)
    if request.method == 'POST':		
		users.name = request.form['name']
		users.phone_number = request.form['phone_number']
		users.email = request.form['email']
		users.address = request.form['address']
		users.table = request.form['table']
		db.session.add(users)
		db.session.commit()
		flash ('Edited')
		return  redirect(url_for('dashboard'))
    return render_template('edit.html', users=users, id=id)

##############################################################################
#Delete 
@app.route('/delete/<id>' , methods=['POST', 'GET'])
@login_required
def delete(id):
	user = User.query.get(id)
	db.session.delete(user)
	db.session.commit()
	flash ('Deleted')
	return redirect(url_for('dashboard'))

#################################################################################
#Admin add users
@app.route('/admin_insert', methods=['GET', 'POST'])
@login_required
def insert():
	error = None
	if request.method == 'POST':
		name = request.form['name']
		phone_number = request.form['phone_number']
		email = request.form['email']
		address = request.form['address']
		table = request.form['table']
		if not name or not email:
			error = "Please check your entires"
			if not phone_number.isdigit():
				error = "Please enter a valid Phone Number"
		user_reg = User(name,phone_number,email,address,table)
		db.session.add(user_reg)
		db.session.commit()
		flash('Registration Successfull.')
	return render_template('admin_insert.html',error = error)
	
###################################################################################	
if __name__ == '__main__':
	app.run(debug = True) 