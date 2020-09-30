#!/usr/bin/env python
# coding: utf-8

# In[22]:


import sys,re
from collections import defaultdict

def pcfg(tree,dic):
    mark = defaultdict(int)
    child = defaultdict(list)
    for i,tag in enumerate(tree):
        st = tag.count("(")
        en = tag.count(")")
        if st==1:
            mark[i]=1
        else:
            child[i-1].append(i)
            temp = i-1
            for j in range(en):
                mark[temp]=0
                for k in range(i,1,-1):
                    if mark[k-2]==1:
                        child[k-2].append(temp)
                        temp = k-2
                        break
    for key,value in child.items():
        par = tree[key].strip("()")
        chi = " ".join([tree[i].strip("()") for i in value])
        dic[par][chi]+=1
    return dic

def normalize(dic):
    for par in dic:
        total = sum([dic[par][chi] for chi in dic[par]])
        for chi in dic[par]:
            dic[par][chi]=dic[par][chi]/total
    return dic

def count_category(prob,words):
    bi,uni,lexi = 0,0,0
    for par in prob:
        for chi in prob[par]:
            if chi in words:
                lexi+=1
            elif len(chi.split())==1:
                uni+=1
            else:
                bi+=1
    print("# of binary rules: %d"%bi)
    print("# of unary rules: %d"%uni)
    print("# of lexical rules: %d"%lexi)
    
if __name__ == "__main__":
    train_tree = sys.stdin.readlines()
    words = open("train.dict").read()
    prob = defaultdict(lambda: defaultdict(float))
    start = train_tree[0].split()[0].strip("()")
    for tree in train_tree:
        tree = tree.strip().split()
        prob = pcfg(tree,prob)
    prob = normalize(prob)
    # count_category(prob,words)
    print(start)
    for par in prob:
        for chi in prob[par]:
            print("%s -> %s # %.4f"%(par,chi,prob[par][chi]))


