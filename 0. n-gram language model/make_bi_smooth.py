import sys
from collections import Counter

weight = dict()
count= dict()

smoothing = 0.5
l1 = ["@"]
l2 = [" ", "\n"]
for i in range(ord('a'), ord('z')+1):
    l1.append(chr(i))
    l2.append(chr(i))
for i in l1:
    for j in l2:
        key = (i, j)
        count[key] = smoothing
# for i, j in zip(*[l1, l2]):
#     key = (i, j)
#     count[key] = smoothing

# print(count)
for line in sys.stdin.readlines():
    line = "@" + line
    frequency = Counter((x, y) for x, y in zip(*[line[i:] for i in range(2)]))
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

# print(weight)

print("F")
print("(0 (<s> <s>))")
for tok, pos in sorted(list(weight.items())):
    tok = list(tok)
    
    for i in range(2):
        if tok[i] == "@":
            tok[i] = "<s>"
        elif tok[i]==" ":
            tok[i] = "_"
        elif tok[i]=="\n":
            tok[i]="</s>"
        else:
            tok[i] = tok[i]
        ini_state = tok[0]

    det_state = tok[1]
    ini_state = tok[0]

    if tok[0]=="<s>":
        print("(<s> ({} {} {:.10f}))".format(det_state, det_state, pos))
    print("({} ({} {} {:.10f}))".format(ini_state, "F", det_state,pos) if det_state == "</s>" else
         "({} ({} {} {:.10f}))".format(ini_state, det_state, det_state, pos))