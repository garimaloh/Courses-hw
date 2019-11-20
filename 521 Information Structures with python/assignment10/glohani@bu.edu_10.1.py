# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 18:57:03 2019

@author: GARIMA
"""
print("Enter the grades of students with a single space on one line please")

a = [int(x) for x in input().split()]
print(a)


g=max(a)
c=-1
for i in a:
 c+=1
 if (i>=(g-10)):
  print("Student",c,"scores is",i,"and grade is A") 
 if (i>=(g-20)and i<(g-10)):   
  print("Student",c,"scores is",i,"and grade is B")   
 if (i>=(g-30)and i<(g-20)):  
  print("Student",c,"scores is",i,"and grade is C")  
 if (i>=(g-40)and i<(g-30)): 
  print("Student",c,"scores is",i,"and grade is D")
 if (i<g-40):
  print("Student",c,"scores is",i,"and grade is F")