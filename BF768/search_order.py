#!/usr/bin/python
# worked with Carol and Stackoverflow
import pymysql
import sys
import cgi
import json
import re
import cgitb

cgitb.enable()

# print content-type
print("Content-type: text/html\n")

print("<html><head>")
print("<title>Search Orders</title>")
print('''<html>
<body style="background-color:powderblue;">
<style>
#ord {
  border-collapse: collapse;
  width: 35%;
  text-align: left;
}
#ord td, #ord th {
  border: 1.5px solid black;
  padding: 2px;
}
</style>
</body>
</html> ''')

form = cgi.FieldStorage()

print("<fieldset><h1>Search Orders</h1>")
print('''<form action="https://bioed.bu.edu/cgi-bin/students_20/glohani/search_order.py" method="POST" >
<br>''')
print('''<P> <label> Order ID: <input type="text" name="order_id" value=""> <P>''') 
query = "SELECT id, name FROM Product;"
print('''Product: <select name='product'/>''')

connection = pymysql.connect(user="glohani", password="lohani", db="glohani", port=4253)
cursor = connection.cursor()
cursor.execute(query)
connection.commit()
records = cursor.fetchall()
 
for p in records:
    print("<option value=%i>%s</option>" % (p[0], p[1]))
print("</select>")
print('''
	 <P>Person name: <input type="text" value="" name="name"><br/><P>
	<p> Date from: <input type="text" name="date_from"   placeholder="yyyy-mm-dd" > 
	&nbsp; &nbsp; to: <input type="text" name="date_to"  placeholder="yyyy-mm-dd" ></p>
	<br>
	&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<input type="submit" value="Go">
	</form>''')
print('''<table id=ord>''')
print('''<tr><th>ID</th><th>Person Name</th><th>Product</th>
	<th>Quantity</th><th>Date</th></tr></fieldset>''')

#cgi form
if form:
 #checking for valid order id 
 form_order_id = form.getvalue("order_id")       
 if form_order_id != None:
        id = 'Orders.id = "%s"' % form_order_id
 else:
	
	id = ''
 #checking for valid product values
 form_product = form.getvalue("product")
 if form_product != None:
	pct = 'Product.id = "%s"' % form_product
 else:
	
	pct = ''
 #checking for valid person name
 form_name = form.getvalue("name") 
 if form_name != None:
        pn = 'person_name like "%s" ' % form_name
 else:
	
	pn = ''
 # checking for valid start date
 form_date_start = form.getvalue("date_from")
 if form_date_start != None:
	date_start = 'date > "%s"' % form_date_start
 else:
	
	date_start = ''
 #checking valid values for end date
 form_date_end = form.getvalue("date_to") 
 if form_date_end != None:
	date_end = 'date < "%s"' % form_date_end
 else:
	date_end = ''
 #checking valid values for date
 if form_date_start != None and form_date_end !=None and form_date_start>= form_date_end:
  print('<p><font color=red><b>Error</b> Invalid date interval </font>') 
 query_value = [id, pn, pct, date_start, date_end]
 
 
 add=[] # creating a list to capture fields in where clause
 for a in query_value:
    if a!='':
     add.append(a)
     

 if query_value != ['','','','','']:
        

    query = """SELECT Orders.id, person_name, name, quantity, date FROM Orders  join Product  ON Orders.product_id = Product.id WHERE %s ORDER BY Orders.id;"""% (' and '.join(add))
    
    rec = 0
    #print(query)
    cursor.execute(query)
    connection.commit()
    rec = cursor.fetchall()
    

    for r in rec:
        
        print("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (r[0], r[1], r[2], r[3],str(r[4])))
    

print("</body></html>")





