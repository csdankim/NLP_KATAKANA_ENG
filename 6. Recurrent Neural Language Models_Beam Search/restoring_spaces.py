from nlm import NLM
from math import log
import sys
from tqdm import tqdm

if __name__ == "__main__":
    NLM.load('base')

    h = NLM()
    b = 20
    for line in tqdm(sys.stdin):
        beam = [(0, h)]
        # line = line.replace("\n", "")
        for c in tqdm(list(line[:-1]) + ["</s>"]):
            newbeam = []
            for score, state in beam:
                newscore = score + log(state.next_prob(c))
                newstate = state + c
                newbeam.append((newscore, newstate))

                newscore = score + log(state.next_prob("_")) + log((state + "_").next_prob(c))
                newstate = state + "_" + c
                newbeam.append((newscore, newstate))

            # choose top b
            beam = sorted(newbeam, reverse=True)[:b]
        score, state = beam[0]
        # print(score)
        # print(state.history)
        print("".join(state.history[1:-1]).replace("_", " "))