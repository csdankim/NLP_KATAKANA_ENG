from nlm import NLM
from math import log
import sys

if __name__ == "__main__":
    NLM.load('base')

    # entropy
    p = 0
    l = 0
    for line in sys.stdin:
    # for line in open('test.txt', 'r').readlines():
        line = line.strip().replace(" ", "_")
        h = NLM()
        for c in line:
            p += -log(h.next_prob(c), 2)
            h += c
        p += -log(h.next_prob("</s>"), 2)
        l += len(line) + 1
    print(p / l)