#! C:\Users\GARIMA\Anaconda3\python.exe

print("Content-Type: text/html;charset=utf-8")
print("")
import cgitb
cgitb.enable()

import MySQLdb
conn = MySQLdb.connect('localhost','garima','garima','library')

cur = conn.cursor()

sql="INSERT INTO books (author,copies,pages) VALUES ('RK','200','3000')"


cur.execute(sql)

cur.close()

conn.close()