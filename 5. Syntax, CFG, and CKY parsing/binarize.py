#!/usr/bin/env python
# coding: utf-8

# In[39]:


import sys,re
from collections import defaultdict

def binarize(tree):
    tree = tree.strip().split()
    if len(tree)==0:
        return
    mark = defaultdict(int)
    node = defaultdict(int)
    last_child = defaultdict(int)
    parent = defaultdict(int)
    for i,tag in enumerate(tree):
        st = tag.count("(")
        en = tag.count(")")
        if st==1:
            mark[i]=1
        else:
            node[i-1]+=1
            parent[i]=i-1
            temp = i-1
            for j in range(en):
                mark[temp]=0
                last_child[temp]=i
                for k in range(i,1,-1):
                    if mark[k-2]==1:
                        node[k-2]+=1
                        parent[temp]=k-2
                        temp = k-2
                        break
    if max(node.values())<3:
        return " ".join(tree)
    else:
        nodes = sorted(node.items(),key=lambda x:x[0])
        nd,child = nodes[0]
        if child<=2:
            tree[last_child[nd]] = tree[last_child[nd]][:-1]
            if tree[last_child[nd+1]+1:]:
                return tree[nd]+" "+binarize(" ".join(tree[nd+1:last_child[nd+1]+1]))+" "+binarize(" ".join(tree[last_child[nd+1]+1:]))+")"
            else:
                return tree[nd]+" "+binarize(" ".join(tree[nd+1:last_child[nd+1]+1]))+")"
        else:
            
#  par is the parent of problem node(cur)                
#  cur is the problem node(more than two children)                
#  res is the name of new node add to tree
#  ind is the position for new node
#  last is the position of the last leaf for this multi-branch node
            res = (tree[nd] if tree[nd][-1]=="'" else tree[nd]+"'")
            ind = last_child[nd+1]+1
            last = last_child[nd]
            tree.insert(ind,res)
            if tree[ind:]:
                return tree[nd]+" "+binarize(" ".join(tree[nd+1:ind]))+" "+binarize(" ".join(tree[ind:]))+")"
            else:
                return tree[nd]+" "+binarize(" ".join(tree[nd+1:ind]))+")"
                

if __name__ == "__main__":
    train_tree = sys.stdin.readlines()
    for tree in train_tree:
        tree = binarize(tree)
        print(tree)


# In[ ]:




