import sqlite3
#Connecting to the database
conn = sqlite3.connect('knowledgeBase.db')
c = conn.cursor()

sql = "DELETE FROM knowledgeBase;"

c.execute(sql)

rows = c.fetchall()
for row in rows:
    del row
conn.commit()
