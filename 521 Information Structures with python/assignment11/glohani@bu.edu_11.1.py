# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 20:12:08 2019

@author: GARIMA
"""

print("list of integers")

a = [int(x) for x in input().split()]
print(a)

b = [int(x) for x in input().split()]
print(b)

c = [int(x) for x in input().split()]
print(c)

d = [int(x) for x in input().split()]
print(d)

m=[a,b,c,d]
def sumColumn(m,columnindex):
 sum=m[0][columnindex] +m[1][columnindex]+m[2][columnindex] +m[3][columnindex]  
 print("Sum of the elements for column",columnindex,"is",sum) 
 
sumColumn(m,0)
sumColumn(m,1)
sumColumn(m,2)
sumColumn(m,3)