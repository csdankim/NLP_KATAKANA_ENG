#!/usr/bin/env python
# coding: utf-8

# In[20]:


# 1.The algorithm for jpron to english word is below:
# Firstly, from jpron to epron: probably there are some potential words which has same pronunciation with epron,
# if there is, record the highest probability(probability of jpron to epron times probability of epron to word) for this epron, 
# and go through other epron from same jpron, if there is new observed word has higher probability than recorded one, replace it. 
# After all eprons from this current jpron sequence, there should have two branch of jpron, one is add a new jpron symble to 
# previous jpron sequence, and another is start a new jpron sequence. For first branch, if there is a word observed from that 
# jpron sequence, record highest probability of that jpron sequence, and start branchs. And for second branch, once there is a 
# word generated from new jpron sequence, use that probability times probability of previous word. Repeat those two branch until 
# the end of the jpron. And choose the branch which has highest probability.
# 2.Subproblem of it is seeking the combination of jpron sequence, and for each jpron sequence find the best english word output
# and comapre probability from different combination of jpron sequence. For each new word generated from current jpron there 
# should have two recurrence, one is based on previous jpron sequence add an addtional jpron, another is starting a new tree of 
# rest of the jpron.
# 3.Time complexity of this problem is O(T^3), spcae complexity is O(T^3)
# 
#NOTE: We don't have eword.probs file instead we have eword.wfsa file as substitution of eword.probs file.






import sys,re,bisect
import numpy as np
from collections import defaultdict

K = 60

def find_k_best(best,k):
    ans = []
    res = []
    #find k_best in last state:
    for epro in best[len(best)-1]:
        for score in best[len(best)-1][epro]:
            if score[1] not in [x[1] for x in res]:
                if len(res)<k: 
                    bisect.insort(res,score)
                else:
                    bisect.insort(res,score)
                    res = res[1:]
            else:
                bisect.insort(res,score)
                for x in res:
                    if x[1]==score[1]:
                        res.remove(x)
                        break
    res = res[::-1]
    for data in res:
        ans.append((data[0],data[1].replace("<s>","").strip()))
    return ans
    
def jpron_to_epron(katakana,ej_dic,etri_dic,K):    
    for pros in katakana:
        best = defaultdict(lambda: defaultdict(list))
        best[0]["<s> <s>"] = [(1,"")]
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
                        for k_best in best[k][prev]:
                            score = k_best[0]*ej_dic[res][epro]*etri_dic[prev][epro]
                            for j in range(i-k):
                                if len(best[k+1+j][prev.split()[1]+" "+epro])<K:
                                    best[k+1+j][prev.split()[1]+" "+epro]+=[(score,k_best[1]+" "+epro)]
                                else:
                                    best[k+1+j][prev.split()[1]+" "+epro].sort(key=lambda x:x[0])
                                    if score > best[k+1+j][prev.split()[1]+" "+epro][0][0]:
                                        best[k+1+j][prev.split()[1]+" "+epro]=best[k+1+j][prev.split()[1]+" "+epro][1:]+[(score,k_best[1]+" "+epro)]






#                             score = k_best[0]*ej_dic[res][epro]*etri_dic[prev][epro]
#                             current_pro = k_best[1].strip()+" "+epro
#                             eword_score,eword = max([(eword_probs[eword],eword) for eword in eword_epron[current_pro]],default=(0,""))
#                             word_score[i] = max(word_score[i-1],eword_score*score)
#                             word_best[i] = (eword if eword_score*score >= word_score[i-1] else word_best[i])
#                             for j in range(i-k):
#                                 if eword:
#                                     best[k+1+j]["<s> <s>"]=[(1,"")]
#                                 if len(best[k+1+j][prev.split()[1]+" "+epro])<K:
#                                     best[k+1+j][prev.split()[1]+" "+epro]+=[(score,k_best[1]+" "+epro)]
#                                 else:
#                                     best[k+1+j][prev.split()[1]+" "+epro].sort(key=lambda x:x[0])
#                                     if score > best[k+1+j][prev.split()[1]+" "+epro][0][0]:
#                                         best[k+1+j][prev.split()[1]+" "+epro]=best[k+1+j][prev.split()[1]+" "+epro][1:]+[(score,k_best[1]+" "+epro)]
                                                

        n = len(best)-1
        for prev in best[n]:
            for k_best in best[n][prev]:
                score = k_best[0]*etri_dic[prev]["</s>"]
                if len(best[n+1][prev.split()[1]+" "+epro])<K:
                    best[n+1][prev.split()[1]+" </s>"]+=[(score,k_best[1])]
                else:
                    best[n+1][prev.split()[1]+" </s>"].sort(key=lambda x:x[0])
                    if score > best[n+1][prev.split()[1]+" </s>"][0][0]:
                        best[n+1][prev.split()[1]+" </s>"]=best[n+1][prev.split()[1]+" </s>"][1:]+[(score,k_best[1])]
        return find_k_best(best,K)
    
def epron_to_eword(eprons,eword_probs,eword_epron,ans):
    score = 0
    word_list = []
    for epron_score,epron in eprons:
        epron_combine = []
        best_word = "ERROR: NO OUTPUT FOR IT!"
        epron = epron.split()
        for i in range(1,len(epron)+1):
            epron_combine.append((epron[:i],epron[i:]))
        for pro in epron_combine:
            pro1,pro2 = " ".join(pro[0])," ".join(pro[1])
            if (pro1 in eword_epron) and (pro2 in eword_epron or pro2 == []):
                for word1 in eword_epron[pro1]:
                    for word2 in eword_epron[pro2]:
                        if score < eword_probs[word1]*eword_probs[word2]*epron_score:
                            score = eword_probs[word1]*eword_probs[word2]*epron_score
                            word_list = [word1,word2]
    print("%s # %e"%(" ".join(word_list),score))    

    
    
katakana = sys.stdin.readlines()
ej_dic = defaultdict(lambda: defaultdict(float))
etri_dic = defaultdict(lambda: defaultdict(float))
epron,e_jpron = open('epron.probs').readlines(),open(sys.argv[3]).readlines()
for line in e_jpron:
    line = re.split(":|#",line.strip())
    ej_dic[line[1].strip()][line[0].strip()] = float(line[2])
for line in epron:
    line = re.split(":|#",line.strip())
    etri_dic[line[0].strip()][line[1].strip()] = float(line[2])


# #save data in dicts
training_data = open(sys.argv[2]).readlines() 
eword_data = open(sys.argv[1]).readlines()
eword_epron = defaultdict(list) #each word aline to some eprons
eword_probs = defaultdict(float)
for line in training_data:
    line = line.strip().split()
    eword_epron[" ".join(line[1:])].append(line[0])
for line in eword_data[1:]:
    line = re.split(" \(| ",line.strip("\)\(\n"))
    eword_probs[line[2]]=float(line[3])
#find 1-best word
eprons = jpron_to_epron(katakana,ej_dic,etri_dic,K)


# def split_string(str1,ans=[]):
#     if len(str1)==1:
#         ans.append(str1)
#     else:
#         for i in range(1,len(str1)+1):
#             res = str1[:i]+split_string(str1[i:],ans)
#             ans.append(res)
# a = split_string(["P","I","A","N","O"])
# print(a)



                
epron_to_eword(eprons,eword_probs,eword_epron,[])
    

