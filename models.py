from app import db


# import sys

class User(db.Model):
	__tablename__ = "users"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), primary_key=False)
	phone_number = db.Column(db.String(100), primary_key=False)
	email = db.Column(db.String(100), primary_key=False)
	address = db.Column(db.String(100), primary_key=False)
	table = db.Column(db.String(100), primary_key=False)
	
	def __init__(self, name, phone_number,email,address,table):
		self.name = name
		self.phone_number = phone_number
		self.email = email
		self.address = address
		self.table = table




def __repr__(self):
        return '<Post %r>' % (self.body)

