# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 19:13:07 2019

@author: GARIMA
"""

#students answer to the questions
answers=[
        ['A','B','A','C','C','D','E','E','A','D'],
        ['D','B','A','B','C','A','E','E','A','D'], 
        ['E','D','D','A','C','B','E','E','A','D'],
        ['C','B','A','E','D','C','E','E','A','D'],
        ['A','B','D','C','C','D','E','E','A','D'],
        ['B','B','E','C','C','D','E','E','A','D'],
        ['B','B','A','C','C','D','E','E','A','D'],
        ['E','B','E','C','C','D','E','E','A','D']]
        
keys=['D','B','D','C','C','D','A','E','A','D']
dic={}
for i in range(len(answers)):
    correctcount=0
    for j in range(len(answers[i])):
        if answers[i][j]==keys[j]:
         correctcount+=1
    print("Student",i,"correct count is ",correctcount)     
    dic[i]=correctcount
print("\n")
import operator
sorted_d = sorted(dic.items(), key=operator.itemgetter(1))
for i in sorted_d:
    print("Student",i[0],"correct count is ",i[1])