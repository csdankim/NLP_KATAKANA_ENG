#!/usr/bin/env python

import sys, itertools, re


dic = dict()
for line in sys.stdin.readlines():    
    temp = re.split(r'\s', line)


    start = 0
    trans = ""
    
    for char in temp:
        if start not in dic:
            dic[start] = set()
        
        trans += char 
        
        dic[start].add(trans)
        start = trans
    
    dic[start] = set([1])

# Do the printing following the FSA format    
print(1)
for key, tok in dic.items():
    for state in tok:
        if state == 1:
            print("({} ({} {} {}))".format(key, state, "*e*", "*e*"))
        else:
            if str(state)[-1] in {"A", "E", "I", "O", "U"}:
                print("({} ({} {} {}))".format(key, state, str(state)[-1], "*e*"))
            else:
                print("({} ({} {} {}))".format(key, state, str(state)[-1], str(state)[-1]))

print("(1 (0 _ _))")          
