#!/usr/bin/env python
# coding: utf-8

# In[37]:


import sys,re
from collections import defaultdict

def cky(sentence,start,pcfg):
    n = len(sentence)
    best = defaultdict(lambda: defaultdict(lambda: defaultdict(float)))
    table = defaultdict(lambda: defaultdict(list))
    back = defaultdict(lambda: defaultdict(lambda: defaultdict(str)))
    for i,word in enumerate(sentence,1):
        temp = []
        for X in pcfg:
            if word in pcfg[X]:
                best[i-1][i][X] = pcfg[X][word]
                back[i-1][i][X] = ('terminal',word)
                temp.append(X)
        flag = True
        while flag:
            flag = False
            for X in pcfg:
                for Y in pcfg[X]:
                    if Y in best[i-1][i]:
                        score = pcfg[X][Y]*best[i-1][i][Y]
                        if score > best[i-1][i][X]:
                            best[i-1][i][X] = score
                            back[i-1][i][X] = ('uni',Y)
                            flag = True
                        
    for span in range(2,n+1):
        for j in range(n-span+1):
            i = j+span
            for k in range(j+1,i):
                for X in pcfg:
                    for chi in pcfg[X]:
                        YZ = chi.split()
                        if len(YZ)==2:
                            Y,Z = YZ[0],YZ[1]
                            if Y in best[j][k] and Z in best[k][i]:
                                score = best[j][k][Y]*best[k][i][Z]*pcfg[X][chi]
                                if score > best[j][i][X]:
                                    best[j][i][X] = score
                                    back[j][i][X] = (k,chi)
            flag = True
            while flag:
                flag = False
                for X in pcfg:
                    for Y in pcfg[X]:
                        if Y in best[j][i]:
                            score = pcfg[X][Y]*best[j][i][Y]
                            if score > best[j][i][X]:
                                best[j][i][X] = score
                                back[j][i][X] = ('uni',Y)
                                flag = True 
                            
    return best,back

def back_track(back,parent,start,end):
    split,child = back[start][end][parent]
    if split=='uni':
        del back[start][end][parent]
        return " ("+child+back_track(back,child,start,end)+")"
    elif split=="terminal":
        return " "+child+")"
    else:
        left,right = child.split()[0],child.split()[1]
        return " ("+left+back_track(back,left,start,split)+" ("+right+back_track(back,right,split,end)+")"

def debinarized(tree):
    flag=False
    res = []
    count = 0 
    tree = tree.split()
    for i,tag in enumerate(tree):
        sta = tag.count("(")
        end = tag.count(")")
        count+=(sta-end)
        if "'" in tag and sta!=0 and flag==False:
            count=1
            flag=True
        elif count<0:
            res.append(tag[:-1])
            res+=tree[i+1:]
            break
        else:
            res.append(tag)
    if count<0:
        return debinarized(" ".join(res))
    else:
        return " ".join(tree)
    
def read_pcfg(pcfg):
    start,pcfg = pcfg[0].strip(),pcfg[1:]
    prob = defaultdict(lambda: defaultdict(float))
    for line in pcfg:
        par,chi,score = tuple(re.split(" # | -> ",line.strip()))
        prob[par][chi]=float(score)  
        
    return start,prob

if __name__ == "__main__":
    sentences = sys.stdin.readlines()
    pcfg_file = open(sys.argv[1]).readlines()
    train_dict = []
    if len(sys.argv)==3:
        train_dict = open(sys.argv[2]).readlines()
    start,pcfg = read_pcfg(pcfg_file)
    train_dict = [word.strip() for word in train_dict]
    for sentence in sentences:
        origin_word = []
        sentence = sentence.strip().split()
        if train_dict:
            for i,word in enumerate(sentence):
                if word not in train_dict:
                    sentence[i] = "<unk>"
                    origin_word.append(word)
        best,back = cky(sentence,start,pcfg)
#         print(best[0][len(sentence)])
        if back[0][len(sentence)]:
            tree = "("+start
            tree += back_track(back,start,0,len(sentence))
            tree = debinarized(tree)
            for word in origin_word:
                tree = tree.replace("<unk>",word,1)
            print(tree)
        else:
            print('NONE')





