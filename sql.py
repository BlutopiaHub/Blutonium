import sqlite3

conn = sqlite3.connect('data.db')
c = conn.cursor()


c.execute("CREATE TABLE prefixes VALUES (id INTEGER, prefix TEXT)")