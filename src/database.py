import mysql.connector 

database = mysql.connector.connect(
    host='localhost',
    user='root',
    port = 3306,
    password='',
    database='banco_mdl'
)

