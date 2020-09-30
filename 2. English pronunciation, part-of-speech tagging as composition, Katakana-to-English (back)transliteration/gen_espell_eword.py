#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys

print("F")
for line in sys.stdin.readlines():
    line = line.strip().split()
    word = line[0]
    ini_state = 0
    det_state = ""
    for letter in word:
        det_state += letter
        print("(%s (%s %s %s))"%(ini_state,det_state,letter,"*e*"))
        ini_state = det_state
    print("(%s (%s %s %s))"%(ini_state,"F","*e*",ini_state))

