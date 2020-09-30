#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys,re,collections
from collections import defaultdict
bigram = open('bigram.wfsa','r').readlines()
lexicon = open('lexicon.wfst','r').readlines()
ptag = {}
wtag = {}
sentences = sys.stdin.readlines()
best = defaultdict(lambda: defaultdict(float))
best[0]["0"]=1
back = defaultdict(dict)
for line in bigram[1:]:
    line = re.split(" |\(",line.strip("(|)\n"))
    key,val,pro = line[0],line[2],float(line[4])
    if key not in ptag:
        ptag[key]={val:pro}
    else:
        ptag[key][val] = pro
    
for line in lexicon[1:]:
    line = re.split(" |\(",line.strip("(|)\n"))
    key,val,pro = line[3],line[4],float(line[5])
    if key not in wtag:
        wtag[key]={val:pro}
    else:
        wtag[key][val] = pro
for words in sentences:
    words = words.strip().split()
    for i,word in enumerate(words,1):
        pword = wtag[word]
        for tag in pword.keys():
            for prev in best[i-1]:
                if tag in ptag[prev]:
                    score = best[i-1][prev]*ptag[prev][tag]*pword[tag]
                    if score > best[i][tag]:
                        best[i][tag] = score
                        back[i][tag] = prev
        if i==len(words):
            for prev in best[i]:
                if "END" in ptag[prev]:
                    score = best[i][prev]*ptag[prev]["END"]
                    if score > best[i+1]["END"]:
                        best[i+1]["END"]=score
                        back[i+1]["END"]=prev

def backward(i,tag):
    if i==0:
        return []
    return backward(i-1,back[i][tag])+[tag]
print(backward(len(words)+1,"END")[:-1],"probability%f"%best[len(words)+1]["END"])

