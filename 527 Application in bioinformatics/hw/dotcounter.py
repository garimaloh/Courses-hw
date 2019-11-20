#3.3A
c=0
A = "GGGAC"
B = "CGGAC"
for i in range(len(A)):        #for loop of len of A string
 for j in range(len(B)):       #for loop of len of B string 
  if(A[i]==B[j]):              #checking for a match
   c+=1                        #counting matches
   if (c==1):
    print("Matches:\n")         
    print("A" , i+1 , "and" , "B", j+1,"\n")
   else:
    print("A", i+1 , "and","B" , j+1, "\n")  

print("Total matches:","\n",c)        

#3.3B
c=0
A = "ACTTGGCCAT"             
B = "AGTAGCGCCT"
for i in range(len(A)):       #for loop of len of A string
 for j in range(len(B)):     #for loop of len of B string 
  if(A[i]==B[j]):            #checking for a match
   c+=1                      #counting matches
   if (c==1):
    print("Matches:\n")
    print("A" , i+1 , "and" , "B", j+1,"\n")
   else:
    print("A", i+1 , "and","B" , j+1, "\n")  
        
print("Total matches:","\n",c)
   
   
 
    
    
    