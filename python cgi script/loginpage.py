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

uname =form.getvalue('username')
passwd = form.getvalue('password')

if "username" not in form or 'password' not in form:
   print ("""
<style>
body {background-color:#f9d2d2 ;}
</style>

<html>
<title>biological database</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Raleway">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style><b>
body,h1 {font-family: "Raleway", Arial, sans-serif}
h1 {letter-spacing: 6px}
.w3-row-padding img {margin-bottom: 12px}
</style></b>
<body>

<!-- !PAGE CONTENT! -->
<div class="w3-content" style="max-width:1500px">

<!-- Header -->
<header class="w3-panel w3-center w3-opacity" style="padding:50px 16px">
  <font size="5"><h1 class="w3-xxxlarge">BIOLOGICAL DATABASE</h1></font>
  <h1>PERSON</h1>
  
   <div class="w3-padding-14" style="background-color:	#66ccff;>
    <div class="w3-bar w3-border">
      <a href="wel2 - Copy.html" class="w3-bar-item w3-button">HOME</a>
	  <a href="home.html" class="w3-bar-item w3-button">ABOUT</a>
      <a href="searchform2.html" class="w3-bar-item w3-button">SEARCH</a>
      <a href="reg2.html" class="w3-bar-item w3-button w3-hide-small">REGISTER</a>
      <a href="login2.html" class="w3-bar-item w3-button w3-hide-small">LOGIN</a>
  <a href="faq.html" class="w3-bar-item w3-button w3-hide-small">HELP</a>
  <a href="con2.html" class="w3-bar-item w3-button w3-hide-small">CONTACT</a>
    </div><br></br> <br></br> 
  <!-- Header -->
<div class="w3-container w3-content w3-center w3-padding-64" style="background-color:#f0f0f0" style="max-width:800px" id="band">
  <h1>LOGIN</h1>
  <p>Pleasee fill in all the details</p>
  <form action="login2.html"> 
  <input type="submit" value="Back">
</form>

</div>
</header>
</html>""")
else:
 try:
    connection = mysql.connector.connect(host='localhost',
                                         database='demo',
                                         user='GARIMA',
                                         password='root')
    cur = connection.cursor()
   

    if connection.is_connected():

        db_Info = connection.get_server_info()
        sql=("SELECT * FROM fnames where username='%s' AND password='%s'")%(uname,passwd)
        cur.execute(sql)
        record = cur.fetchall()
        if (len(record)>0):
         st=("Hello %s, Welcome to our website.You are succesfully logged in. Thankyou")%(uname)
         
        else :
            st=("Sorry, you are not registered.Please register.")
            
        
            
 except Error as e:
    print("Error while connecting to MySQL", e)
 finally:
    if (connection.is_connected()):
        cur.close()
        connection.close()
        
 print("""<html>
 <style>
 body {background-color: #f9d2d2;}
</style>
<title>biological database</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Raleway">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
<style><b>
body,h1 {font-family: "Raleway", Arial, sans-serif}
h1 {letter-spacing: 6px}
.w3-row-padding img {margin-bottom: 12px}
</style></b>
<body>

<!-- !PAGE CONTENT! -->
<div class="w3-content" style="max-width:1500px">

<!-- Header -->
<header class="w3-panel w3-center w3-opacity" style="padding:50px 16px">
  <font size="5"><h1 class="w3-xxxlarge">BIOLOGICAL DATABASE</h1></font>
  <h1>PERSON</h1>
  
   <div class="w3-padding-14" style="background-color:	#66ccff;>
    <div class="w3-bar w3-border">
      <a href="wel2 - Copy.html" class="w3-bar-item w3-button">HOME</a>
	  <a href="home.html" class="w3-bar-item w3-button">ABOUT</a>
      <a href="searchform2.html" class="w3-bar-item w3-button">SEARCH</a>
      <a href="reg2.html" class="w3-bar-item w3-button w3-hide-small">REGISTER</a>
      <a href="login2.html" class="w3-bar-item w3-button w3-hide-small">LOGIN</a>
  <a href="faq.html" class="w3-bar-item w3-button w3-hide-small">HELP</a>
  <a href="con2.html" class="w3-bar-item w3-button w3-hide-small">CONTACT</a>
    </div><br></br> <br></br> 
  <!-- Header -->
<div class="w3-container w3-content w3-center w3-padding-64" style="background-color:#f0f0f0" style="max-width:800px" id="band">

  <h1>LOGIN</h1>
  <p>%s </p>
  <form action="login2.html">
  <input type="submit" value="Back">
  </div>
</header>
 </html>""" %st)
