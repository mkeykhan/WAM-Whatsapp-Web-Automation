import mysql.connector as mysql

# Database info
HOST = 'mysql.gb.stackcp.com'
PORT = 56073
DATABASE = 'thewamdb-3231341eb7'
USER = "wamuser"
PASSWORD = "€`No;Y!spqVb"

try:
    db_connection = mysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, db=DATABASE)
    print("Connected to:", db_connection.get_server_info())
    c = db_connection.cursor()
    connection = 1
except:
    connection = 0
    print(connection)