import mysql.connector

def get_connection():
    return mysql.connector.connect(
        user = 'admin',
        host = 'localhost',
        database = 'mydb',
        password = 'admin'
        )

