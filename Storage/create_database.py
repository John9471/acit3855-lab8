import mysql.connector

conn = mysql.connector.connect(host="acit3855.eastus2.cloudapp.azure.com", user="user", password="password", database="events")
c = conn.cursor()
c.execute('''
          CREATE TABLE inventory
          (id INT NOT NULL AUTO_INCREMENT, 
           name VARCHAR(250) NOT NULL,
           contents VARCHAR(250) NOT NULL,
           price INTEGER NOT NULL,
           date_created DATETIME NOT NULL,
           CONSTRAINT inventory_pk PRIMARY KEY (id))
          ''')

c.execute('''
          CREATE TABLE profit
          (id INT NOT NULL AUTO_INCREMENT, 
           companyName VARCHAR(250) NOT NULL,
           quantity INTEGER NOT NULL,
           drink VARCHAR(250) NOT NULL,
           date_created DATETIME NOT NULL,
           CONSTRAINT profit_pk PRIMARY KEY (id))
          ''')

conn.commit()
conn.close()