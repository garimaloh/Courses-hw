#! C:\Users\GARIMA\AppData\Local\Programs\Python\Python37-32\python.exe
# -*- coding: UTF-8 -*-# enable debugging
import cgitb
import cgi
cgitb.enable()
print("Content-Type: text/html;charset=utf-8")
print("")

import mysql.connector
from mysql.connector import Error

form = cgi.FieldStorage()
query= form.getvalue('query')

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='demo',
                                         user='GARIMA',
                                         password='root')
    cur = connection.cursor()
   

    if connection.is_connected():

        db_Info = connection.get_server_info()
        sql="SELECT*FROM fnames WHERE username LIKE'%s'" %(query)
        cur.execute(sql)
        record=cur.fetchall()
        print(record)
        
            
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if (connection.is_connected()):
        cur.close()
        connection.close()
        print("MySQL connection is closed")
