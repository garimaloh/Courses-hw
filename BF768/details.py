#!/usr/local/Python-3.7/bin/python

import cgi
import pymysql

form = cgi.FieldStorage()
if form:

    connection = pymysql.connect(host='bioed.bu.edu',db='glohani',user='glohani',password='glohani',port=4253)
    cursor = connection.cursor()

    submit = form.getvalue("submit")
    
    if submit:
       
        p_name = form.getvalue("product_name")
        query = """
        SELECT name,quantity,price 
        FROM Products
        WHERE name = "%s" 
        """ % p_name
        cursor.execute(query)
        rows=cursor.fetchall()

        print("Content-type: text/html\n")
        for row in rows:
            print(row[0]+"\t"+str(row[1])+"\t"+str(row[2]))

    else:
        table = form.getvalue("table")

        if table == "category":
            query = """
            SELECT category 
            FROM Categories
            """
        else: 
            
            if table == "product":
                c_name = form.getvalue("category_name")      
                query = """
                SELECT name 
                FROM Products join Categories using(cid)
                WHERE category = '%s'
                """%(c_name)

        
        cursor.execute(query)
        rows=cursor.fetchall()

        print("Content-type: text/html\n")
        for row in rows:
            print(row[0])

else:
    print("Content-type: text/html\n")
