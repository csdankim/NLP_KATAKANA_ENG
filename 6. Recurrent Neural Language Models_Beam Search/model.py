import torch
import torch.nn as nn
import torch.nn.functional as F


class RNNModel(nn.Module):

    def __init__(self, args):
        super(RNNModel, self).__init__()
        if args.one_hot:
            self.emb_size = args.vocab_size
            self.emb = nn.Embedding(args.vocab_size, args.vocab_size)
            self.emb.weight.data = torch.eye(args.vocab_size)
            self.emb.weight.requires_grad = False
        else:
            self.emb_size = args.emb_size
            self.emb = nn.Embedding(args.vocab_size, args.emb_size)
        self.drop = nn.Dropout(args.dropout)
        if args.rnn_type in ['RNN', 'LSTM', 'GRU']:
            self.rnn = getattr(nn, args.rnn_type)(
                args.emb_size, args.hidden_size, args.layer_num, batch_first=True)
        else:
            raise ValueError("""Invalid option, options ['LSTM', 'RNN', 'GRU']""")
        self.fc = nn.Linear(args.hidden_size, args.vocab_size)
        if args.weight_tie:
            self.fc.weight = self.emb.weight
        self.hidden_size = args.hidden_size
        self.device = args.device
        

    def makeMask(self, outputs, seq_len):
        seq_mask = torch.zeros(outputs.size())
        for i, _seq_len in enumerate(seq_len):
            seq_mask[i][0:int(_seq_len)] = 1
        return torch.Tensor(seq_mask)

    def init_hidden(self, bz=1, layer_num=1):
        return (torch.zeros(layer_num, bz, self.hidden_size).to(self.device),
                torch.zeros(layer_num, bz, self.hidden_size).to(self.device))

    def forward(self, x, hidden):
        emb_input = self.emb(x)
        outputs, hidden = self.rnn(emb_input, hidden)
        # logit = self.fc(self.drop(outputs))
        # return logit, hidden
        return hidden
