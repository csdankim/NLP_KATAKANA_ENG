#!/usr/bin/env python
# coding: utf-8

# In[ ]:
import sys,re

dic = {}
weight = {}#The times of a letter after a specific state
sum_weight = {}#The total times of a state appears
vowel = ['A','E','I','O','U']
#each line in strings has several words
for line in sys.stdin.readlines():
#split each words by "_"
    for word in line.strip().split("_"):
        ini_state = 0
        det_state = ""
#find path for each word and count the times
        for letter in word.strip().split():
            det_state+=letter
            if ini_state not in dic:
                dic[ini_state]=set()
                sum_weight[ini_state] = 0
            if (ini_state,letter) not in weight:
                weight[(ini_state,letter)]=0
            dic[ini_state].add(det_state)
            sum_weight[ini_state]+=1
            weight[(ini_state,letter)]+=1
            ini_state=det_state
        if ini_state not in dic:
            dic[ini_state]=set(['1'])
        else:
            dic[ini_state].add('1')
        if ini_state not in sum_weight:
            sum_weight[ini_state]=0
        if (ini_state,'1') not in weight:
            weight[(ini_state,'1')]=0
        weight[(ini_state,'1')]+=1
        sum_weight[ini_state]+=1
print('1')
for key,value in sorted(list(dic.items()),key=lambda x:len(str(x[0]))):
    for state in value:
        pos = float(weight[(key,str(state)[-1])])/float(sum_weight[key])
        if state=='1':
            res = "(%s (%s %s %s %f))"%(key,state,"*e*","*e*",pos)
        elif str(state)[-1] not in vowel:
            res = "(%s (%s %s %s %f))"%(key,state,str(state)[-1],str(state)[-1],pos)
        else:
            res = "(%s (%s %s %s %f))"%(key,state,str(state)[-1],"*e*",pos)
                
        print(res)
print("(1 (0 _ _ 1.0))")