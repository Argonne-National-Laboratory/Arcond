# Arcond v1.0
# S.Chekanov (ANL)
# Correct number of cores in case on-fly 


import os,sys,shutil
import glob
import time


def nrcores(DIR,PWD,MaxJobsPerNode): 
  print "---> Final checking computing cores"

  Err=0
  DEBUG=False
  for  l  in os.listdir(DIR):
        l=l.strip()
        if not l.endswith(".conf"):  continue
        ifile = open(DIR+l,'r')
        newlines = []
        for xline in ifile:
                  xline=xline.strip()
                  if xline.startswith("#"):        continue
                  ii=xline.find("CPU_N");
                  if ii>-1 and MaxJobsPerNode>0:
                      xline="CPU_N="+str(MaxJobsPerNode) 
                  newlines.append(xline+"\n")
        ifile.close()
        outfile = file(DIR+l, 'w')
        outfile.writelines(newlines) 
        outfile.close()

  return Err
