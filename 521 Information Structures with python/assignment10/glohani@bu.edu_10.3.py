# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 19:16:53 2019

@author: GARIMA
"""

print("list of integers")

a = [int(x) for x in input().split()]
print(a)
b={}
for i in a:
    b[i] = b.get(i, 0) + 1

for keys in b:
    if (b[keys]>1):
     print( keys, "occurs" ,b[keys], "times" )
    if (b[keys]==1): 
     print( keys, "occurs" ,b[keys], "time" )