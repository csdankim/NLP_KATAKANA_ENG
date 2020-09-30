#!/usr/bin/env python

from __future__ import division

import sys
from collections import defaultdict

counts = match = 0.
for line1, line2 in zip(open(sys.argv[1]), open(sys.argv[2])):
    words1 = line1.strip().split()
    words2 = line2.strip().split()
    for word1, word2 in zip(words1, words2):
        counts += 1
        if word1 == word2:
            match += 1
    
print("word acc= %.3f" % (match / counts))
