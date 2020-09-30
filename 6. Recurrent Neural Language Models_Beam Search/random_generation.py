from nlm import NLM

if __name__ == "__main__":
    NLM.load('huge')

    # random generation
    h = NLM("p o r t l a n d _ o r e g o n")
    t = 0.5
    import random
    for _ in range(10):
        h = NLM("p o r t l a n d _ o r e g o n")
        chars = list(h.next_prob().keys())
        # print(chars)
        while chars != "</s>":
            probs = h.next_prob()
            #s = sum(p ** (1/t) for p in probs.values())
            probs = {c: p ** (1/t) for (c, p) in probs.items()}
            [choice] = random.choices(chars, [probs[c] for c in chars])
            print(choice, end=' ')
            h += choice
            if choice == "</s>":
                print()
                h = NLM()
                break
        print()