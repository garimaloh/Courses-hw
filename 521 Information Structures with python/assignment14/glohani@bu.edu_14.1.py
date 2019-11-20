# -*- coding: utf-8 -*-
"""
Created on Sun Feb 17 13:45:10 2019

@author: GARIMA
"""

import os.path
import sys
def main():
    keywords={"and","as","assert","break","class","continue","def","del","elif","else","except","False","finally","for","from","global","if","import","in","is","lambda","None","nonlocal","not","or","pass","raise","return","True","try","while","with","yield"}
    filename=input("Enter a Python source code filename:").strip()
    if not os.path.isfile(filename):
        print("File",filename,"does not exist")
        sys.exit()
    infile=open(filename,"r")
    text.infile.read().split()
    count=0
    for word in text:
        if words in keywords:
            count+=1
            print(words)
    print("The number of the keywords in",filename,"is",count)

main()        