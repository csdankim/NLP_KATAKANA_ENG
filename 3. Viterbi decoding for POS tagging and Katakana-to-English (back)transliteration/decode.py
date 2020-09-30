#!/usr/bin/env python
# coding: utf-8
# In[537]:
import sys,re
from collections import defaultdict



# print 1-best

def find_best(best,back):
    ans = []
    for i in range(len(best)-1,0,-1):
        if i==len(best)-1:
            temp = sorted(best[i].items(),key=lambda x:x[1],reverse=True)[0][0]
            b_score = sorted(best[i].items(),key=lambda x:x[1],reverse=True)[0][1]
            if temp in back[i]:
                ans = [temp.split()[1]]
                temp = back[i][temp]
        else:
            if temp in back[i]:
                ans.append(temp.split()[1])
                temp = back[i][temp]
    ans.pop(0)
    print("%s # %.6e"%(" ".join(list(reversed(ans))),b_score))
    
katakana = sys.stdin.readlines()
epron,e_jpron = open(sys.argv[1],"r").readlines(),open(sys.argv[2],"r").readlines()
ej_dic = defaultdict(lambda: defaultdict(float))
etri_dic = defaultdict(lambda: defaultdict(float))
for line in e_jpron:
    line = re.split(":|#",line.strip())
    ej_dic[line[1].strip()][line[0].strip()] = float(line[2])
for line in epron:
    line = re.split(":|#",line.strip())
    etri_dic[line[0].strip()][line[1].strip()] = float(line[2])
    
for pros in katakana:
    best = defaultdict(lambda: defaultdict(float))
    back = defaultdict(dict)
    best[0]["<s> <s>"] = 1
    back[0]["<s> <s>"] = "<s> <s>"
    pros = pros.strip().split()
    for i in range(1,len(pros)+1):
        temp = []
        for k in range(i-1,i-4,-1):
            if (k<0):
                continue
            temp = [pros[k]]+temp
            res = " ".join(temp)
            for epro in ej_dic[res]:
                for prev in best[k]:
                    score = best[k][prev]*ej_dic[res][epro]*etri_dic[prev][epro]
                    for j in range(i-k):
                        if score > best[k+1+j][prev.split()[1]+" "+epro]:
                            best[k+1+j][prev.split()[1]+" "+epro]=score
                            back[i-j][prev.split()[1]+" "+epro]=prev
    n = len(best)-1
    for prev in best[n]:
        score = best[n][prev]*etri_dic[prev]["</s>"]
        if score > best[n+1][prev.split()[1]+" </s>"]:
            best[n+1][prev.split()[1]+" </s>"]=score
            back[n+1][prev.split()[1]+" </s>"]=prev
    find_best(best,back)