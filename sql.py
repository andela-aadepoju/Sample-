import sqlite3

with sqlite3.connect("user.db") as connectiion:
	
	c = connectiion.cursor()
	
	c.execute("DROP TABLE users")
	c.execute("CREATE TABLE users(ID INT, name TEXT, phone_number TEXT, email TEXT, address TEXT, table TEXT)")
	  