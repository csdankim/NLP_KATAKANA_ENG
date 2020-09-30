#!/usr/bin/env python
# coding: utf-8



import sys
import re

print("0")
for line in sys.stdin.readlines():
    line = re.split(":|#",line.strip())
    e_state = line[0].strip()
    prob = float(line[-1])
    k_states = line[1].strip().split()
    k_state = ("_").join(list(e_state) + k_states)
    ini_state = ""
    for i,k in enumerate(k_states):
        det_state = k_state+str(i)
        if i==0:
            print("(0 (%s %s %s %f))"%(det_state,e_state,k,prob))
            ini_state=det_state
        else:
            print("(%s (%s %s %s 1.0))"%(ini_state,det_state,"*e*",k))
            ini_state=det_state
    print("(%s (%s))"%(ini_state,"0"))
