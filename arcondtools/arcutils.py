# Arcond v1.6
# S.Chekanov (ANL)
# Util functions 

import os,sys
import glob

#  get list of files 
def getFiles(rootdir):
  fileList = []
  for root, subFolders, files in os.walk(rootdir):
    for file in files:
        fileList.append(os.path.join(root,file))
  return fileList


# Break a list into roughly equal sized pieces.
"""
def split_seq(seq, size):
        newseq = []
        splitsize = 1.0/size*len(seq)
        for i in range(size):
                newseq.append(seq[int(round(i*splitsize)):int(round((i+1)*splitsize))])
        return newseq

"""

# This version uses integer math and distributes the remaindered items evenly over the first few splits.
def split_seq(seq, p):
    newseq = []
    n = len(seq) / p    # min items per subsequence
    r = len(seq) % p    # remaindered items
    b,e = 0, n + min(1, r)  # first split
    for i in range(p):
        newseq.append(seq[b:e])
        r = max(0, r-1)  # use up remainders
        b,e = e, e + n + min(1, r)  # min(1,r) is always 0 or 1

    return newseq
