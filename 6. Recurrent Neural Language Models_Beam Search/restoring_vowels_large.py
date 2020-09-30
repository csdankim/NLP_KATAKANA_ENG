from nlm import NLM
from math import log
import sys
from tqdm import tqdm

if __name__ == "__main__":
    NLM.load('large')

    VOWELS = ['a', 'e', 'i', 'o', 'u']
    MAX_REPEAT = 2
    h = NLM()
    b = 40

    for line in tqdm(sys.stdin):
        # for line in open('test.nowowels.txt', 'r').readlines():
        beam = [(0, h)]
        line = line.replace(" ", "_")
        for c in tqdm(list(line[:-1]) + ["</s>"]):
            newbeam = []
            prev = [beam]
            for i in range(MAX_REPEAT + 1):
                tmp = []
                for score, state in prev[-1]:
                    newscore = score + log(state.next_prob(c))
                    newstate = state + c
                    newbeam.append((newscore, newstate))
                    if i <= MAX_REPEAT:
                        for vowel in VOWELS:
                            newscore = score + log(state.next_prob(vowel))
                            newstate = state + vowel
                            tmp.append((newscore, newstate))
                prev.append(tmp)

            # choose top b
            beam = sorted(newbeam, reverse=True, key=lambda x: x[0])[:b]

        score, state = beam[0]
        # print(score)
        print("".join(state.history[1:-1]).replace("_", " "))