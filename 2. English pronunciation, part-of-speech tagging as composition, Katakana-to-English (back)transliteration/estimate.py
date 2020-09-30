#!/usr/bin/env python
# coding: utf-8

# In[36]:


import sys
import numpy as np

weight_e = {}
weight_ej = {}
data = open("epron-jpron.data","r").readlines()
for i in range(0,len(data),3):
    epro = data[i].strip().split()
    jpro = data[i+1].strip().split()
    index = list(map(int,data[i+2].strip().split()))
    index=index-np.ones_like(index)
    temp = ""
    ans = ""
    for k in epro:
        if k not in weight_e:
            weight_e[k]=1
        else:
            weight_e[k]+=1
    for j_ind,e_ind in enumerate(index):
        if j_ind==0:
            ans = epro[e_ind]+":"+jpro[j_ind]
            temp = e_ind
        elif temp==e_ind:
            ans+=" "+jpro[j_ind]
        else:
            if ans not in weight_ej:
                weight_ej[ans]=1
            else:
                weight_ej[ans]+=1
            temp=e_ind
            ans = epro[e_ind]+":"+jpro[j_ind]
    if ans not in weight_ej:
        weight_ej[ans]=1
    else:
        weight_ej[ans]+=1

for key,value in weight_ej.items():
    epro = key.split(":")[0]
    if len(key.split())>3:
        continue
    probab = float(value)/float(weight_e[epro])
    if probab<0.001:
        continue
    print("%s # %f"%(key,probab))




