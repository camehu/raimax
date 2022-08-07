import mysql.connector
from mysql.connector import errorcode
from mysql.connector import (connection)
try:
	db_connection = mysql.connector.connect(host="us-cdbr-east-06.cleardb.net", user="b6914c23389c6b", password="cd8edf81", database="heroku_a7f279a8e4d980e")
	conn = db_connection.cursor()
	db_conn = connection.MySQLConnection(host="us-cdbr-east-06.cleardb.net", user="b6914c23389c6b", password="cd8edf81", database="heroku_a7f279a8e4d980e")
	db_connection.close()

except mysql.connector.Error as error:
	if error.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database doesn't exist")
	elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("User name or password is wrong")
	else:
		print(error)
else:
	db_connection.close()
