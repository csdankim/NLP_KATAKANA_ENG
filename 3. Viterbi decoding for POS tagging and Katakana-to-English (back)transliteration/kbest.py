import sys,re,bisect
import numpy as np
from collections import defaultdict

K = 5

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
        print("%s # %.6e"%(data[1].replace("<s>","").strip(),data[0]))


katakana = sys.stdin.readlines()
ej_dic = defaultdict(lambda: defaultdict(float))
etri_dic = defaultdict(lambda: defaultdict(float))
epron,e_jpron = open(sys.argv[1],"r").readlines(),open(sys.argv[2],"r").readlines()
for line in e_jpron:
    line = re.split(":|#",line.strip())
    ej_dic[line[1].strip()][line[0].strip()] = float(line[2])
for line in epron:
    line = re.split(":|#",line.strip())
    etri_dic[line[0].strip()][line[1].strip()] = float(line[2])
    
    
for pros in katakana:
#     btype = [("PREV",str),("SCORE",float)]
    best = defaultdict(lambda: defaultdict(list))
    back = defaultdict(dict)
    best[0]["<s> <s>"] = [(1,"<s> <s>")]
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
                    for k_best in best[k][prev]:
                        score = k_best[0]*ej_dic[res][epro]*etri_dic[prev][epro]
                        for j in range(i-k):
                            if len(best[k+1+j][prev.split()[1]+" "+epro])<K:
                                best[k+1+j][prev.split()[1]+" "+epro]+=[(score,k_best[1]+" "+epro)]
                            else:
                                best[k+1+j][prev.split()[1]+" "+epro].sort(key=lambda x:x[0])
                                if score > best[k+1+j][prev.split()[1]+" "+epro][0][0]:
                                    best[k+1+j][prev.split()[1]+" "+epro]=best[k+1+j][prev.split()[1]+" "+epro][1:]+[(score,k_best[1]+" "+epro)]
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
    find_k_best(best,K)
    