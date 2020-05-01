#!/usr/local/Python-3.7/bin/python

import cgi
import pymysql

form = cgi.FieldStorage()
if form:
    connection = pymysql.connect(host='bioed.bu.edu',db='glohani',user='glohani',password='glohani',port=4253)
    cursor = connection.cursor()
    submit = form.getvalue("submit")
    customer = form.getvalue("customer")
    if submit and customer!=None:
        product = form.getvalue("product")
        quantity = form.getvalue("quantity")
        
        query1 = "SELECT pid FROM Products WHERE name='%s'" % product
        cursor.execute(query1)
        result=cursor.fetchall()
        pid = result[0][0]

        query2 = """
        INSERT INTO Orders(pid,customer,quantity)
        VALUES(%d,"%s",%d)
        """ % (int(pid),str(customer),int(quantity))
        cursor.execute(query2)
        connection.commit()
        
        query3 = '''UPDATE Products
                    SET quantity=quantity-%d
                    WHERE pid=%d''' % (int(quantity),int(pid))
        cursor.execute(query3)
        connection.commit()

        print("Content-type: text/html\n")
        print(customer+", your order is placed "+str(quantity)+" "+product+"!")
    
    
