#!/usr/bin/env python
# coding: utf-8

# In[246]:


import sys,re,math
from collections import defaultdict
from itertools import permutations

K = 5

def initialize(epron,jpron,fractional):
    enum,jnum = len(epron),len(jpron)
    res =[]
    for tri in range (enum+1):
        for duo in range(enum+1):
            for single in range(enum+1):
                if tri*3+duo*2+single == jnum and tri+duo+single == enum:
                    temp=[3]*tri+[2]*duo+[1]*single
                    temp = permutations(temp)
                    res+=(list(set(temp)))
# should consider all epron-jpron together, and give probability to each
    for seq in res:
        temp=0
        for i,j in enumerate(seq):
            fractional[epron[i]][" ".join(jpron[temp+k] for k in range(j))]+=(1/len(res))
            temp+=j
    return fractional
    
def forward_backward(epron,jpron,ej_dic,fractional,totalprob):
#     alpha
    forward = defaultdict(lambda: defaultdict(float))
#     beta
    backward = defaultdict(lambda: defaultdict(float))
    n,m = len(epron),len(jpron)
    forward[0][0] = 1
    backward[n][m]=1
# initialize part
#forward calculation 
    for i in range(0,n):
        for j in forward[i]: 
# m-j: the number of the rest jpron
            for k in range(1,min(m-j-n+i+1,m-j,3)+1):
                jseg = " ".join(jpron[j:j+k])
                if epron[i] in ej_dic.keys():
                    prob_ej = (ej_dic[epron[i]][jseg] if jseg in ej_dic[epron[i]].keys() else 0.001)
                else:
                    prob_ej = 0.001
                score = forward[i][j]*prob_ej
                forward[i+1][j+k] += score
# totalprob: corpus probability (times each example's final probability)                
    totalprob *= forward[n][m]
#backward calculation 
    for i in range(n,0,-1):
        for j in backward[i]:
            for k in range(1,min(j-i+1,j+1,3)+1):
                count = min(j-i+1,j,3)
                jseg = " ".join(jpron[j-k:j])
                if epron[i-1] in ej_dic.keys():
                    prob_ej = (ej_dic[epron[i-1]][jseg] if jseg in ej_dic[epron[i-1]].keys() else 0.001)
                else:
                    prob_ej = 0.001
                score = backward[i][j]*prob_ej
                backward[i-1][j-k] += score

#fraccount part
    for i in range(n):
        for u in forward[i]:
            for v in backward[i]:
                if u>=v+1 or v+1-u>=3:
                    continue
                else:
                    if epron[i] in ej_dic.keys():
                        prob_ej = (ej_dic[epron[i]][" ".join(jpron[u:v+1])] if " ".join(jpron[u:v+1]) in ej_dic[epron[i]].keys() else 0.001)
                    else:
                        prob_ej = 0.001
                    fractional[epron[i]][" ".join(jpron[u:v+1])] += ((forward[i][u]*backward[i+1][v+1]*prob_ej))/forward[n][m]
    
    return fractional,totalprob

def output_probs_file(prob):
    for e in prob:
        for j in prob[e]:
            if prob[e][j]>=0.01:
                print("%s : %s # %f"%(e,j,prob[e][j]))
                
if __name__ == "__main__":
    ej_data = sys.stdin.readlines()
    #ej_data = open("epron-jpron.data").readlines()
# list of paried epron-jpron data
    epron_jpron = []
# dictionary for epron-jpron probability
    ej_dic = defaultdict(lambda: defaultdict(float))
    for i in range(0,len(ej_data),3):
        epron,jpron = ej_data[i].strip().split(),ej_data[i+1].strip().split()
        epron_jpron.append((epron,jpron))
    for iteration in range(K):
        new_prob = defaultdict(lambda: defaultdict(float))
        fractional = defaultdict(lambda: defaultdict(float))
        fractional[0]["<s>"] = 1
        totalprob = 1
        if iteration==0:
            for epron,jpron in epron_jpron:
                fractional = initialize(epron,jpron,fractional)
        else:
            for epron,jpron in epron_jpron:
                fractional,totalprob = forward_backward(epron,jpron,ej_dic,fractional,totalprob)
        for e in fractional:
            total = sum([fractional[e][j] for j in fractional[e]])
            for j in fractional[e]:
                if (fractional[e][j]/total)<0.01:
                    continue
                else:
                    new_prob[e][j] = fractional[e][j]/total
        ej_dic = new_prob
    output_probs_file(ej_dic)
#     print(totalprob) 

    
    


# In[ ]:




