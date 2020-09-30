import sys,re
from collections import defaultdict



def viterbi(epron,jpron,ej_dic):
    best = defaultdict(lambda: defaultdict(float))
    align = defaultdict()
#   best[i][j], best probability for epron is ith and jprob is jth.  
    best[0]["0"] = 1
    align[0] = 0
    for i in range(1,len(epron)+1):
        for j in best[i-1]:
#start_j first jpron for this align, end_j last jpron for this align
            end_j = int(j.split()[-1])
            temp = []
            for k in range(end_j+1,end_j+4):
                if k-1<0 or k-1>=len(jpron):
                    continue
                temp+=[jpron[k-1]]
                res = " ".join(temp)
                prob_ej = (ej_dic[res][epron[i-1]] if epron[i-1] in ej_dic[res].keys() else 0.0001)
                score = best[i-1][j]*prob_ej
#                 print(k,j)
#                 if score>max([best[p][k] for p in best if k in best[p]],default=0):
                if score>best[i][" ".join([str(h) for h in range(end_j+1,k+1)])]:
                    best[i][" ".join([str(h) for h in range(end_j+1,k+1)])]=score
                    
    return best

def find_best_align(best,k):
    align = []
    temp = 10000
    for i in range(len(best)-1,0,-1):
        if i==len(best)-1:
            res = sorted(best[i].items(), key=lambda x:-x[1])
            best_score,jnum = max([(j[1],j[0]) for j in res if str(k) in j[0]])
            align+=([str(i)]*len(jnum.split()))
            temp = int(jnum.split()[0])
        else:
            best_score = 0
            res = sorted(best[i].items(), key=lambda x:-x[1])
            for jnum,score in res:
                if score>=best_score and temp-int(jnum.split()[-1])==1:
                    best_score = score
                    align+=([str(i)]*len(jnum.split()))
                    temp=int(jnum.split()[0])
    
    return(align[-1::-1])        
            
           
if __name__ == "__main__":
    ej_probs = open(sys.argv[1]).readlines()
    ej_data = sys.stdin.readlines()
# list of paried epron-jpron data
    epron_jpron = []
# dictionary for epron-jpron probability
    ej_dic = defaultdict(lambda: defaultdict(float))
    for i in range(0,len(ej_data),3):
        epron,jpron = ej_data[i].strip().split(),ej_data[i+1].strip().split()
        epron_jpron.append((epron,jpron))
    for line in ej_probs:
        line = re.split(":|#",line.strip())
        ej_dic[line[1].strip()][line[0].strip()] = float(line[2]) 
    for sample_num,(epron,jpron) in enumerate(epron_jpron):
        align = []
        if len(epron)==len(jpron):
            align=[str(i) for i in range(1,len(jpron)+1)]
        else:
            best = viterbi(epron,jpron,ej_dic)
            align = find_best_align(best,len(jpron))
        ej_data[2+3*sample_num]=" ".join(align)
    for data in ej_data:
        print(data.strip())
    