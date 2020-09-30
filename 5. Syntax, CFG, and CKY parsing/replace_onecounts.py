#!/usr/bin/env python
# coding: utf-8

# In[23]:


import re,sys,bisect
from collections import defaultdict

def dict_generate(tree):
    dic = defaultdict(int)
    for line in tree:
        temp = []
        line = re.split(" ",line.strip())
        for cont in line:
            count = 0
            if cont[0]=="(":
                continue
            for cha in cont:
                if cha!=")":
                    count+=1
                else:
                    break
            temp.append(cont[:count])
        for word in temp:
            dic[word]+=1
    dic_items = sorted(dic.items(),key=lambda x:x[1])
    dic_values = sorted(dic.values())
    spli_idx = bisect.bisect_left(dic_values,2)
    dic_uni = dict(dic_items[:spli_idx])
    dic = dict(dic_items[spli_idx:])
#     dic is words count dict exclude one-counted word, dic_uni is one-counted words dict
    return dic,dic_uni

# def uni_replace(tree,dic):
#     ans = []
#     for line in tree:
#         temp = []
#         res = re.split(" ",line.strip())
#         for cont in res:
#             count = 0
#             if cont[0]=="(":
#                 continue
#             for cha in cont:
#                 if cha!=")":
#                     count+=1
#                 else:
#                     break
#             temp.append(cont[:count])
#         for word in temp:
#             if word in dic.keys():
#                 line = line.replace(word,"<unk>")
#         ans.append(line)    
#     return "".join(ans)

def uni_replace(tree,dic):
    res = re.split(" ",tree.strip())
    for i,cont in enumerate(res):
        tag = cont.strip("()")
        if tag in dic:
            res[i]=cont.replace(tag,"<unk>")
    return " ".join(res)        

if __name__ == "__main__":
    train_tree = sys.stdin.readlines()
    train_dict,train_uni_dict = dict_generate(train_tree)
    for tree in train_tree:
        tree_uni = uni_replace(tree,train_uni_dict)
        sys.stdout.write(tree_uni+"\n")
    sys.stderr.write("".join([key+"\n" for key in train_dict.keys()]))
