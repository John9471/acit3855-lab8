import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", password="Alienbanana1", database="lab4")

c = conn.cursor()
c.execute('''
          DROP TABLE inventory, profit
          ''')

conn.commit()
conn.close()