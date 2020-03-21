#!/usr/local/Python-3.7/bin/python
# BF768 HW3
# add_order.py
# worked with Carol and Stackoverflow
#import module to connect to a mysql database
import pymysql
# import cgi
import cgi
# displays errors (if any) in web browser
import cgitb; 
cgitb.enable()


#start the html output
print("Content-type: text/html\n")
print("")

#start the html code
print("<html><head>")
print("<title>Add order query</title>")
print('''</head>''')
print('''<html>
<body style="background-color:powderblue;">
</body>
</html> 
''')
print("<body>")

print("<fieldset><h1>Enter new order</h1>")

# The original page html
try:
    connection = pymysql.connect(user="glohani", password="lohani", db="glohani", port=4253)
    cursor = connection.cursor()
    query="SELECT * FROM Product;"
    cursor.execute(query)
    records = cursor.fetchall()
    cursor.close()
    connection.close()
    
    print(''' <form action="https://bioed.bu.edu/cgi-bin/students_20/glohani/add_order.py"  method ='POST'>
		Product &nbsp   <SELECT name="Product">''')
    # dropbox creates with automatically filled products name.
    for l in records:
        print("<option value =%i>%s</option>" %(l[0],l[1]))
    print('''</SELECT>
             <P>
             quantity &nbsp<INPUT TYPE="number" NAME="quantity" SIZE="4" >
             <P>
             name &nbsp&nbsp&nbsp&nbsp&nbsp<INPUT TYPE="TEXT" NAME="name" SIZE="20">
             <P>
             &nbsp&nbsp &nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp<input type="submit" value="GO">
             </form>''')
# Error message displayed due to wrong execution of input.
except Exception as mysqlError:
	print("<p><font color=red><b>Error</b> Page is unable to load </font></p>")


# retrieve form data, if any
form = cgi.FieldStorage()
form_id = form.getvalue("Product")
form_quantity = form.getvalue("quantity")
form_name = form.getvalue("name")



# Function for execute query
def execute_query(query):
    connection = pymysql.connect(user="glohani", password="lohani", db="glohani", port=4253)
    cursor = connection.cursor()
    q_1=query
    cursor.execute(q_1)
    res = cursor.fetchall()
    cursor.close()
    connection.close()
    return res

# Function to modify tables
def update_query(query):
    connection = pymysql.connect(user="glohani", password="lohani", db="glohani", port=4253)

    cursor = connection.cursor()
    q_1=query
    cursor.execute(q_1)
    connection.commit()
    cursor.close()
    connection.close()


if form_quantity and form_name:
    try:
        rec_stock = execute_query("SELECT stock FROM Product WHERE Product.id = %s;" % (form_id, ))
        rec_name = execute_query("SELECT name FROM Product WHERE Product.id = %s;" % (form_id, ))
        stock = rec_stock[0][0];
        name = rec_name[0][0];
        # This is the message for any order smaller than the stock amount.
        
        if stock >= int(form_quantity) and int(form_quantity)!=0:
                # This is the command to update the product stock number. 
                up_stock = stock - int(form_quantity)
                update_query("UPDATE Product SET Product.stock= %i WHERE Product.id = %i; " %(up_stock, int(form_id)))
                # This is the command to add a new order into the order table.
                update_query("INSERT INTO Orders (person_name, product_id, quantity) VALUES ('%s', %i, %i);" % (str(form_name), int(form_id), int(form_quantity)))
                # This is the message of each successful order.
                print("<p><font color=green><b>Success</b>: Order successfully entered. </font></p>" )
        
        else:
         if stock ==0:
                name = (name + "s").lower()
                print("<p><font color=red><b>Error</b>: Sorry %s, not enough product in stock. Only %i %s available.</font></p>" % (form_name, stock, name ))
         else:
             print("<p><font color=red><b>Error</b>:Enter valid quantity </font></p>" )   
    # This is the message of wrong excecution.
    except Exception as mysqlError:
    	print("<p><font color=red><b>Error</b>:while executing your request</font></p>")

if form_quantity and not form_name:
	print("<p><font color=red> Enter your name!!! </font></p>")
print("</body></html>")

if form_name and not form_quantity:
	print("<p><font color=red> Enter your quantity!!! </font></fieldset></p>")
print("</body></html>")


#end the html code
print("</body></html>")


