#!/usr/bin/env python

from __future__ import division

import sys
from collections import defaultdict

tot1 = match = tot2 = 0
for line1, line2 in zip(open(sys.argv[1]), open(sys.argv[2])):
    words1 = line1.split()
    words2 = line2.split()
    counts1 = defaultdict(int)
    counts2 = defaultdict(int)
    for word in words1:
        counts1[word] += 1
    for word in words2:
        counts2[word] += 1
    for word in counts1:
        tot1 += counts1[word]
        match += min(counts1[word], counts2[word])
    for word in counts2:
        tot2 += counts2[word]
    
print("recall= %.3f precision= %.3f F1= %.3f" % (match / tot1, 
                                                 match / tot2,
                                                 2*match / (tot1+tot2) ))
