import sys, re
from collections import Counter

weight = dict()
count= dict()

# smoothing
smoothing = 0
l1 = [" ","@"]
l2 = [" "]
l3 = [" ","\n"]
for i in range(ord('a'), ord('z')+1):
    l1.append(chr(i))
    l2.append(chr(i))
    l3.append(chr(i))
for i in l1:
    for j in l2:
        for k in l3:
            key = (i, j, k)
            count[key] = smoothing  

for line in sys.stdin.readlines():
    line = "@" + line            # @ == <s>
    frequency = Counter((x, y, z) for x, y, z in zip(*[line[i:] for i in range(3)]))
    for tok, freq in frequency.items():
        if tok not in count:
            count[tok] = freq
        else:
            count[tok] += freq

# print(count)

total_freq = sum(count.values())
for tok, freq in count.items():
    pos = freq / total_freq
    weight[tok] = pos

print("F")
print("(0 (<s> <s>))")
for tok, pos in sorted(list(weight.items())):
    tok = list(tok)

    for i in range(3):
        if tok[i] == "@":
            tok[i] = "<s>"
        elif tok[i]==" ":
            tok[i] = "_"
        elif tok[i]=="\n":
            tok[i]="</s>"
        else:
            tok[i] = tok[i]
    
    ini_state = tok[0]+tok[1]
    det_state = tok[1]+tok[2]

    if tok[0]=="<s>":
        print("(<s> ({} {} {:.10f}))".format("<s>"+tok[1],tok[1],pos))

    print("({} ({} {} {:.10f}))".format(ini_state, "F", tok[2], pos) if tok[2] == "</s>" else
         "({} ({} {} {:.10f}))".format(ini_state, det_state, tok[2], pos))