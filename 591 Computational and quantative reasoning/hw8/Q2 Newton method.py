
# coding: utf-8

# In[1]:


import math
from scipy.misc import derivative

def func_val(x):
    return x*math.exp(-x) - (1/(2*math.pi))

def func_val_sec_root(x):
    global first_root
    return (x*math.exp(-x) - (1/(2*math.pi)))/(x-first_root)

#making initial guess and number of iterations
initial_guess=0
num_of_iter=100

#finding the root through Newton's method after knowing the derivative value
x1=[0 for i in range(num_of_iter)]
x1[0]=initial_guess
for i in range(1,num_of_iter):
    x1[i]=x1[i-1] - func_val(x1[i-1])/(math.exp(-x1[i-1])*(1-x1[i-1]))
    
    
#finding the root through Newton's method even when the derivative is not known    
    
x1=[0 for i in range(num_of_iter)]
x1[0]=initial_guess
for i in range(1,num_of_iter):
    x1[i]=x1[i-1] - func_val(x1[i-1])/(derivative(func_val, x1[i-1], dx=1e-6))
first_root=x1[-1]
    
x2=[0 for i in range(num_of_iter)]
x2[0]=initial_guess
for i in range(1,num_of_iter):
    x2[i]=x2[i-1] - func_val_sec_root(x2[i-1])/(derivative(func_val_sec_root, x2[i-1], dx=1e-6))    
second_root=x2[-1]        
   
    

print("The value of first_root is {}".format(first_root))
print("The value of second_root is {}".format(second_root))
    

    
    
    

