# part of ArCond v1
# S.Chekanov (ANL)


import os,sys,shutil
import glob
import time
from arcondtools.arcutils  import *


def getcentral(term,DIR): 
 
 print "---> Build inputs assuming the central file location"

 REDO=False
# initial processing:
 COMM=[]
 NAME=[]
 DATA=[]
 N_CPU_TOT=0 
 for  l  in os.listdir(DIR):
        l=l.strip()
        if not l.endswith(".conf"):  continue
        lines=[]
        ifile = open (DIR+l,'r')
        lines=lines+ifile.readlines()      # read file into list of lines
        ifile.close()
        comm=[]
        data=[]
        cpus=[] 
        NCPU=0
        for i in range(len(lines)):
                  xline=lines[i]
                  xline=xline.strip()
                  ii=xline.find("CPU_N");
                  if xline.startswith("#") or ii>-1:
                          comm.append(xline)
                  else: 
                          data.append(xline)
                  if (ii>-1):
                            xline=xline[ii+6:len(xline)]
                            NCPU=int(xline);
        cpus.append(NCPU)
        COMM.append(comm)
        NAME.append(l)
        DATA.append(data)
        N_CPU_TOT=N_CPU_TOT+NCPU


# split one file:
 if len(DATA)==0 or DATA[0] == 0:
       print term.render('${RED}ERROR: Could not find necessary data! ${NORMAL}')
       return -1

 Nboxes=len(DATA)

# calculate the notal number of splits we will need 
 DataSplitted=split_seq(DATA[0],Nboxes)

# split in accordance with the number of boxes
 DATA=[]
 for job in range( len(DataSplitted) ):
                Data=DataSplitted[job]
                DATA.append(Data) 


 m=0
 for l in NAME:
       # print l
       ifile = open (DIR+l,'w')
       comm=COMM[m];
       data=DATA[m]
       m=m+1
       for k1 in comm:
            ifile.write(k1+"\n")
       for k2 in data:
            ifile.write(k2+"\n")
       ifile.close() 
          
