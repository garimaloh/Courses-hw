# -*- coding: utf-8 -*-
"""
Created on Wed Sep 19 00:47:36 2018

@author: GARIMA
"""

sequence="acgCUGacCAguCAgccuACUgAAAAA" # The sequence is stored as string type
trim1=sequence.rstrip('A') #rstrip function removes the poly-A tail in the end of the sequence
trim1=trim1.upper()       # convert to upper case to aviod case sensitive issues in the program
for i in range(len(trim1)) : # a loop which finds and prints the location of U in the sequence 
 if(trim1[i] =='U'):        # if condition to check find the 'U' in the sequence
  print(i)