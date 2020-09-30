import sys, re
from collections import Counter

weight = dict()
count= dict()

for line in sys.stdin.readlines():
    frequency = Counter(line)
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
print("(0 (1 <s>))")
for tok, pos in sorted(list(weight.items())):
    if tok == " ":
        print("(1 (1 {} {}))".format("_", pos))
    elif tok == "\n":
        continue
    else:
        print("(1 (1 {} {}))".format(tok, pos))
print("(1 (F </s> {}))".format(weight["\n"]))