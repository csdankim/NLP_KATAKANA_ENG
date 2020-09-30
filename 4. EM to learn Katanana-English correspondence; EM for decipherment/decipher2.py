#!/usr/bin/env python
# coding: utf-8

# In[73]:


#!/usr/bin/env python
# coding: utf-8

import sys
import math
from itertools import permutations
from collections import defaultdict

K = 2 # iteration times

########################################################################
##
##                          Bigram LM
##
########################################################################
def bigram(train_text):
    START, END = ('<s>', '</s>')
    lambdas = [.01, .09, .9]
    with open(train_text) as f:
        lines = f.read().splitlines()
    f.close()
    
    dict_uni = defaultdict(float)
    dict_bi = defaultdict(lambda: defaultdict(float))
    N = 0
    for line in lines:
        chars = [START] + list(line.replace(' ', '_')) + [END]
#         print(chars)
        N += (len(chars)-1)
#         dict_uni[START] += 1
        for i,cha in enumerate(chars):
            dict_uni[cha] += 1
            if i!=0:
                dict_bi[chars[i-1]][cha] += 1
#             dict_bi[START][START] += 1
#         for i in range(2, len(chars)):
#             dict_uni[chars[i]] += 1
#             dict_bi[chars[i-1]][chars[i]] += 1
    
    voc = dict_uni.keys()
    V = len(voc)
    for c1 in voc:
        s1 = ('1' if c1 == START else 'F' if c1 == END else c1)
#         if c1 != END:
        for c2 in voc:
            s2 = ('1' if c2 == START else 'F' if c2 == END else c2)
#                 if c2 != START:
            dict_bi[c1][c2] = (dict_bi[c1][c2]+1) / (dict_uni[c1]+V)
                    
    return dict_bi
    
########################################################################
##
##                              EM
##
########################################################################           
def initialize():
    chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'l', 'n',     'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '_']
    em_prob = defaultdict(lambda: defaultdict(float))
    for hd in chars:
        for obs in chars:
            em_prob[hd][obs] = 1/27
    return em_prob

def normalize(prob):
    new_prob = defaultdict(lambda: defaultdict(float))
    for hd in prob:
        total=sum([prob[hd][obs] for obs in prob[hd]])
        if total == 0:
            for obs in prob[hd]:
                new_prob[hd][obs] = 1/27
        else:
            for obs in prob[hd]:
                if prob[hd][obs] < 0.01:
                    continue
                else:
                    new_prob[hd][obs]=prob[hd][obs]/total
    return new_prob

def getEntropy(prob):
    entropy = 0
    sumEntropy = 0
    uniEntropy = 0
    for hd in prob:
        uniEntropy=sum([prob[hd][obs] for obs in prob[hd]])
        sumEntropy += uniEntrpy
        uniEntropy = 0
    entropy = sumEntropy/27.00
    return entropy

# output iteration logs
def output(prob,k,corpus,entropy):
    count = 0
    for hd in prob:
        res = prob[hd].items()
        print("%s|->  %s"%(format(hd,'<2')," ".join([":".join([i[0],str(round(i[1],2))]) for i in res if i[1]>=0.001])))
        for obs in prob[hd]:
            if prob[hd][obs]>=0.01:
                count+=1
    print("epoch  %d logp(corpus)= %.2f  entropy= %.2f nonzeros= %d"%(k,math.log(2,corpus),entropy,count))

# output probability
def output_probs_file(prob):
    for hd in prob:
        for obs in prob[hd]:
            if prob[hd][obs]>=0.01:
                print("%s : %s # %f"%(hd,obs,prob[hd][obs]))
    
def em(cipher,prob,dict_bi,corpus,fractional):
    n = len(cipher)
    forward = defaultdict(lambda:defaultdict(float))
    backward = defaultdict(lambda: defaultdict(float))
    forward[0]['<s>'] = 1
    backward[n]['</s>'] = 1
    for i,cha in enumerate(cipher,1):
        for prev in dict_bi:
            for hd in prob:
                forward[i][hd]+=(prob[hd][cha]*dict_bi[prev][hd]*forward[i-1][prev])
    for i in range(n,0,-1):
        for hd in prob:
            for fron in dict_bi[hd]:
                backward[i-1][hd]+=(prob[hd][cipher[n-1]]*dict_bi[hd][fron]*backward[i][fron])
    for i in range(n):
        for u in forward[i]:
            for v in backward[i]:
#                 print(sum(forward[i].values()),sum(backward[i+1].values()),prob[u][cipher[i]])
                fractional[u][cipher[i]]+= (((sum(forward[i].values())*sum(backward[i+1].values())*prob[u][cipher[i]]))/sum([forward[n][m] for m in forward[n]]))
                
    return fractional
        

if __name__ == "__main__":
    train_text = "train.txt"
    cipher = open("cipher6.txt").readlines()
    bi_data = defaultdict(lambda: defaultdict(float))
    prob = initialize()
    bi_data = bigram(train_text)
    corpus = 1
    for iteration in range(K):
        fractional = defaultdict(lambda: defaultdict(float))
        fractional[0]["<s>"] = 1
        for line in cipher:
            line = line.strip()
            fractional = em(line,prob,bi_data,corpus,fractional)
        prob = normalize(fractional)
#         print(prob)
        
    output_probs_file(prob)
    
    
    
    
    


# In[ ]:




