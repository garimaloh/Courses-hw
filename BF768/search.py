#!/usr/bin/python
# used w3school template
#image taken from url- https://www.insidehighered.com/sites/default/server_files/media/abstract-background-vector-id905644702_0.jpg
import pymysql
import cgi
import cgitb
cgitb.enable()

print("Content-type: text/html\n")
print("<html>")
print("<head>")
print("<title>Search miRNA</title>")

def execute_query(query):
 connection = pymysql.connect(host="bioed.bu.edu", user="glohani", password="glohani", db="miRNA", port=4253)
 cursor = connection.cursor()
 q1=query
 cursor.execute(q1)
 results = cursor.fetchall()
 cursor.close()
 connection.close()
 return results 

print('''
<html>

<title>W3.CSS Template</title>
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
<!-- !PAGE CONTENT! -->
<!-- Header -->
<div class="w3-content" style="max-width:1500px"  margin: 0; >
<div class="row">
  <div class="column">
    <img src="https://www.insidehighered.com/sites/default/server_files/styles/large-copy/public/media/abstract-background-vector-id905644702_0.jpg?itok=YDNlgnY_" style="width:100%">
  </div>
  <div class="column">
    <img src="https://www.insidehighered.com/sites/default/server_files/styles/large-copy/public/media/abstract-background-vector-id905644702_0.jpg?itok=YDNlgnY_" style="width:100%">
  </div>
  <div class="column">
    <img src="https://www.insidehighered.com/sites/default/server_files/styles/large-copy/public/media/abstract-background-vector-id905644702_0.jpg?itok=YDNlgnY_" style="width:100%">
  </div></div>
  
<header class="w3-panel w3-center w3-opacity" style="padding:0px 0px">
  <font size="5"><h1 class="w3-xxlarge">SEARCH</h1></font>
  <h1>miRNA database</h1>
  <div class="w3-container w3-content w3-center w3-padding-64" style="background-color:#f0f0f0" style="max-width:800px">
  <form onsubmit="return checkEnter();" action="https://bioed.bu.edu/cgi-bin/students_20/glohani/search.py"  method="POST" a href="#">
       Gene Symbol:  <input type="text" id="genename" name="genename">
	 Target Score: <input type="number" step="0.001" id="scores" name="scores">
        <input type="submit" value="Search" >
        </form>
    <center><table id=ord></center>
    <tr><th>miRNA name</th><th> Target score</th></tr></center>
    </center>'
  </div>
</header>
</body>


</html>
''')

print('''<html>
<body style="background-color: #f9d2d2;">
<style>
#ord {
  border-collapse: collapse;
  width: 35%;
  text-align: center;
}
#ord td, #ord th {
  border: 1.5px solid black;
  padding: 2px;
}
.center {
  text-align: center;
  
}
</style>
<style>
* {
  box-sizing: border-box;
}

.column {
  float: left;
  width: 33.33%;
  padding: 0px;
}

/* Clearfix (clear floats) */
.row::after {
  content: "";
  clear: both;
  display: table;
}
</style>
</body>
</html> ''')

genes= execute_query ("select name from gene")
genes = [g[0] for g in genes]
print('''<script type="text/javascript">
        function checkEnter() {
                var name = document.getElementById('genename').value;
		var score = document.getElementById('scores').value;
		var geneset = %s;
                if (name == "") {
                        alert("Please enter a gene name!");
                        return false;
                }
                else if (score == ""){
                        alert("Please enter score!");
                        return false;
                }
		else if (geneset.indexOf(name)==-1) {
			alert("No such gene in the database!");
                        return false;
                }
                else {
                        return true;
                }
        }
        </script>''' % genes)

form = cgi.FieldStorage()
gene = form.getvalue("genename")
scores = form.getvalue("scores")

if form:
    

    query = """SELECT miRNA.name as name, targets.score as score
            FROM miRNA JOIN targets ON (miRNA.mid=targets.mid) JOIN gene ON (targets.gid=gene.gid)
            WHERE gene.name = '%s' and score < %s;""" % (gene,scores)

    try:
        record=execute_query(query)
        for row in record:
            print("<tr><td>%s</td><td>%f</td></tr>" % (row[0], row[1]))
      

    except Exception as mysqlError:
        print("<p>Error while executing query.</p>")

    print("</table>")

print("</body></html>")

