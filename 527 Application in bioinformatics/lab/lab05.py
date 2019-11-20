
mat=[]
begin_number=[]

for i in range(1,12,5):
  begin_number.append(i)
for i in (begin_number):
 row=[]   
 for j in range(i,i+5,1):
   row.append(j) 
 mat.append(row)
for i in range (len(mat)):
 print(mat[i]) 
 
    