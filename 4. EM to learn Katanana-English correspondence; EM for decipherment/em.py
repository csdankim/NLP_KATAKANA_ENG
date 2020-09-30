#!/usr/bin/env python
# coding: utf-8

import sys
from itertools import permutations
from collections import defaultdict
K = int(sys.argv[1]) #iteration times
def initialize(epron,jpron,prob,complete):
    enum,jnum = len(epron),len(jpron)
    res =[]
    for tri in range (enum+1):
        for duo in range(enum+1):
            for single in range(enum+1):
                if tri*3+duo*2+single == jnum and tri+duo+single == enum:
                    temp=[3]*tri+[2]*duo+[1]*single
                    temp = permutations(temp)
                    res+=(list(set(temp)))
# should consider all epron-jpron together, and give probability to each
    for seq in res:
        temp=0
        for i,j in enumerate(seq):
            prob[epron[i]][" ".join(jpron[temp+k] for k in range(j))]+=1
            temp+=j
    complete.append(res)
    return prob,complete

def normalize(prob):
    for e in prob:
        total=sum([prob[e][j] for j in prob[e]])
        for j in prob[e]:
            prob[e][j]=prob[e][j]/total
    return prob
# output iteration logs
def output(prob,k,corpus):
    print("iteration %d ----- corpus prob= %.12f"%(k,corpus))
    count = 0
    for e in prob:
        res = prob[e].items()
        print("%s|->  %s"%(format(e,'<2')," ".join([":".join([i[0],str(round(i[1],2))]) for i in res if i[1]>=0.001])))
        for j in prob[e]:
            if prob[e][j]>=0.01:
                count+=1
    print("nonzeros = %d"%count)
    
# output probability
def output_probs_file(prob):
    for e in prob:
        for j in prob[e]:
            if prob[e][j]>=0.01:
                print("%s : %s # %f"%(e,j,prob[e][j]))
            
def em(prob,new_prob,complete,epron,jpron,corpus):
    regen = []
    fractional = []
    for seq in complete:
        temp=1
        res=0
        for i,jnum in enumerate(seq):
            for jpro in prob[epron[i]]:
                if jpro.split()==jpron[i+res:i+res+jnum]:
                    temp*=prob[epron[i]][jpro]
                    res+=(jnum-1)
                    break
        
        regen.append(temp)
    fractional = [i/sum(regen) for i in regen]

    for p,seq in enumerate(complete):
        temp=0
        for i,jnum in enumerate(seq):
            new_prob[epron[i]][" ".join(jpron[temp+k] for k in range(jnum))]+=(fractional[p])
            temp+=jnum
#     new_prob = normalize(new_prob)
    corpus*=sum(regen)
    return new_prob,corpus

if __name__ == "__main__":
    ej_data = sys.stdin.readlines()
    epron_jpron = []
    for i in range(0,len(ej_data),3):
        epron,jpron = ej_data[i].strip().split(),ej_data[i+1].strip().split()
        epron_jpron.append((epron,jpron))
    prob = defaultdict(lambda: defaultdict(float))
    comp = []
    for epron,jpron in epron_jpron:
        prob,comp = initialize(epron,jpron,prob,comp)
    prob = normalize(prob)
#     output(prob,0,0.004115226337)
    for j in range(1,K):
        new_prob = defaultdict(lambda: defaultdict(float))
        corpus = 1
        for i,(epron,jpron) in enumerate(epron_jpron):
            new_prob,corpus = em(prob,new_prob,comp[i],epron,jpron,corpus)
        prob=normalize(new_prob)
        
#         print(prob)

#         output(prob,j,corpus)
    output_probs_file(prob)
