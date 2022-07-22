import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="aviso-suporte-interno"
)

print(mydb)