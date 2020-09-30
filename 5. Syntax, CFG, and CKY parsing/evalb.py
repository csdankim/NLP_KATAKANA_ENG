#!/usr/bin/env python

''' simplified PARSEVAL.
    author: David Chiang <chiang@isi.edu>, Liang Huang <lhuang@isi.edu>
'''

import sys
logs = sys.stderr

import itertools, collections
from tree import Tree

if __name__ == "__main__":
    try:
        _, parsefilename, goldfilename = sys.argv
    except:
        print >> logs, "usage: evalb.py <parse-file> <gold-file>\n"
        sys.exit(1)

    matchcount = parsecount = goldcount = 0

    for parseline, goldline in itertools.izip(open(parsefilename), open(goldfilename)):
        goldtree = Tree.parse(goldline)
        goldbrackets = goldtree.label_span_counts()    
        goldcount += sum(goldbrackets.values())

        if parseline.strip() == "NONE": # parsing failure
            continue

        parsetree = Tree.parse(parseline)
        parsebrackets = parsetree.label_span_counts()
        parsecount += sum(parsebrackets.values())

        for bracket, count in parsebrackets.iteritems():
            matchcount += min(count, goldbrackets[bracket])

    print "%s\t%d brackets" % (parsefilename, parsecount)
    print "%s\t%d brackets" % (goldfilename, goldcount)
    print "matching\t%d brackets" % matchcount

