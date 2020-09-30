from model import RNNModel

from configparser import ConfigParser
import argparse
import json
import copy
import torch
import torch.nn.functional as F
import sys
import time

class NLM:
    @staticmethod
    def load(model_name): # static
        parser = argparse.ArgumentParser()
        NLM.args = parser.parse_args()
        NLM.VOCABLIST = ['<pad>', '<s>', '</s>', '<unk>', '_'] + [chr(i) for i in range(97,123)]
        NLM.OUTPUTLIST = ['_', '</s>'] + [chr(i) for i in range(97,123)]
        NLM.vocab = {ch:idx for idx, ch in enumerate(NLM.VOCABLIST)}
        NLM.output_vocab = {ch:idx for idx, ch in enumerate(NLM.OUTPUTLIST)}
        NLM.OUTPUTLISTIDX = [NLM.vocab[i] for i in NLM.OUTPUTLIST]
        with open('./saved_models/{}/config.json'.format(model_name), 'r') as rf:
            NLM.args.__dict__ = json.load(rf)
        NLM.args.vocab_size = len(NLM.VOCABLIST)
        NLM.args.device = torch.device('cpu')
        NLM.model = RNNModel(NLM.args) 
        with open('./saved_models/{}/model.pt'.format(model_name), 'rb') as rf:
            NLM.model.load_state_dict(torch.load(rf, map_location='cpu'))

    def __init__(self, xs=None, hidden=None, history=[]): # can supply init string
        if hidden is None:
            self.hidden = NLM.model.init_hidden(1, NLM.args.layer_num)
            self.history = []
            self += '<s>'
            if xs is not None: # init string
                self.__iadd__(xs)
        else:
            self.hidden = hidden
            self.history = history
        self.__repr__ = self.__str__
    
    def __add__(self, xs):
        hidden, history = self.hidden, self.history[:] # copy!
        for x in xs.split():
            x_id = NLM.vocab[x]
            input_ids = torch.Tensor([[x_id]]).long().to(NLM.args.device)
            hidden = NLM.model(input_ids, hidden)
            history.append(x)
        return NLM(hidden=hidden, history=history)

    def __iadd__(self, xs):
        for x in xs.split():
            x_id = NLM.vocab[x]
            input_ids = torch.Tensor([[x_id]]).long().to(NLM.args.device)
            self.hidden = NLM.model(input_ids, self.hidden)
            self.history.append(x)
        return self
    
    def next_prob(self, char=None):
        output = NLM.model.fc(self.hidden[0])
        output = output[-1,-1,:].squeeze() # two layers
        probs = F.softmax(output[NLM.OUTPUTLISTIDX], dim=-1).tolist()
        if char == None:
            return {ch:prob for ch, prob in zip(NLM.OUTPUTLIST, probs)}
        else:
            return probs[NLM.output_vocab[char]]

    def __str__(self):
        d = list(self.next_prob().items())
        return "\"%s\": [%s]" % (" ".join(self.history), ", ".join("%s: %.2f" % (c, p) for (c, p) in sorted(d, key=lambda x: -x[1]) if p>0.01))
        
    ___repr__ = __str__

# def eval(s):
#     h = NLM()
#     p = 0
#     for c in s:
#         p += log(h.next_prob(c))
#         h += c
#     p += log(h.next_prob("</s>"))
#     return p

if __name__ == "__main__":
    NLM.load('huge')

    # evaluate a string
    h = NLM()
    p = 1
    for c in 't h e _ e n d _ '.split():
        print("%.3f" % p, h)
        p *= h.next_prob(c)
        h += c

    # greedy generation
    h = NLM("d o n a l d _ t r u m p ")
    for _ in range(100):
        c, p = max(h.next_prob().items(), key=lambda x: x[1])
        print(c, "%.2f <- p(%s | ... %s)" % (p, c, " ".join(map(str, h.history[-4:]))))
        h += c

    # shannon game
    text = "b  r  o  w  n  _  b  e  a  r  _  w  a  s  _  a  l  l  o  w  e  d  _  i  n  t  o  _  t  h  e  _  c  i  r  c  u  s  _  t  e  n  t  _  w  i  t  h  o  u  t  _  p  a  y  i  n  g  _  b  e  c  a  u  s  e  _ ".split()
    h = NLM()
    guesses = []
    for c in text:
        order = sorted(h.next_prob().items(), key=lambda x: -x[1])
        for i, (char, prob) in enumerate(order):
            if c == char:
                break
        guesses.append(i + 1)
        h += c
    print(" ".join("%2s" % c for c in text))
    print(" ".join("%2d" % g for g in guesses))
    









