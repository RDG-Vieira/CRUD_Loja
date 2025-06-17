import sqlite3

conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM usuarios')
print(cursor.fetchall())
conn.close()