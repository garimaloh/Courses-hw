# -*- coding: utf-8 -*-
"""
Created on Thu Sep 20 22:49:23 2018

@author: GARIMA
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import os
from collections import Counter
from collections import defaultdict

os.getcwd()                           #to find  the current working directory
f=open("v13_map_uniquebyPSN.txt","r")
line=f.readline()
bs=""
bsmales=""
bsfemales=""
samplesf=0
d=defaultdict(str)                 #default dictionary used to store unique value of body site with the sample id
for line in f:
 word=line.split()                 # word separation per line
 if(word[2]=='1'):                 
  samplesf+=1                     # counting the number of sample for first visit
  d[word[5]]+= word[0]+","        # storing values of sample id for the body sites
  bs= bs + ":"+ word[5]           # string collection of body sites
  if (word[3]=="male"):
   bsmales = bsmales+":"+ word[5] #  counting frequency of males
  if (word[3]=="female"):         # counting frequency of female 
   bsfemales = bsfemales +":"+ word[5]  
  
f.close()

print(d)           

with open('samples_id.json', 'w') as fp: # saving the dictionary to file in json format
 json.dump(d, fp)
    
 
print("Total number of samples for first visit:",samplesf) # total samples for site visit

bs=bs.split(":")
bsfemales=bsfemales.split(":")
bsmales=bsmales.split(":")
del bs[0] 
del bsfemales[0] 
del bsmales[0]

samplec=Counter(bs)  # dict consisting of counts of samples for the body sites

b=Counter(bsfemales) # dict consisting of counts of samples for the body sites
bm=Counter(bsmales)   # dict consisting of counts of samples for the body sites

fw=plt.figure(figsize=(50,30))
ax = fw.add_subplot(1, 1, 1)

for keys in b:
    if keys not in bm:        #adding the missed keys
        bm[keys]=0

ax.tick_params(labelsize=20)     # plotting bar plot
ax.set_yticks((0,20,40,60,80,100,120))
ax.set_xticklabels(samplec.keys(), rotation=90, rotation_mode='anchor')
ax.set_ylabel('Frequency',fontsize = 40, fontweight = 'bold')
ax.set_xlabel('Body Sites', fontsize = 40, fontweight = 'bold')
for tick in ax.xaxis.get_major_ticks():
      tick.label1.set_fontweight('bold')
for tick in ax.yaxis.get_major_ticks():
      tick.label1.set_fontweight('bold')
X = np.arange(len(samplec))
ax = plt.subplot(111)
ax.bar(X,samplec.values(),width=0.2,color='lightgreen',align='center')
ax.bar(X-0.2,b.values(),width=0.2,color='pink',align='center')
ax.bar(X-0.4,bm.values(),width=0.2,color='lightblue',align='center')
ax.legend(('Total','Females','Males'))
plt.xticks(X,samplec.keys())
plt.title('Human Microbiome Data', fontsize = 50, fontweight = 'bold') 
plt.show()

fw.savefig("C:/Users/GARIMA/.spyder-py3/plot2.pdf")  # saving to a pdf



