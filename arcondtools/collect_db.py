# This code is licensed under the GNU General Public License (GPL) version 3 
# see doc/ for details 
# Copyright (c) 2008 by S.Chekanov (chakanau@hep.anl.gov). 
# All rights reserved.

# as an argument, pass location of your input files 


__version__ = 'Arcond 1.0'
__author__  = 'Sergei Chekanov  (chakanau@hep.anl.gov)'
__doc__     = 'For details see doc'


import os,sys,re,shutil
import time, glob
import getopt
sys.path.append("./basic/")
from initialize import *


def collect_db(term, PWDdir, DataDir, DEBUG,MaxJobsPerNode):
 """ Collect data from a static database"""

# input directory with database  
 input=ArcDBaseDIR
 # make sure correct search string
 if not DataDir.endswith("/"):
                        DataDir=DataDir+'/'
 
 partten = DataDir


 N_PC=1
 nodes=[]
 jj=len("machine")
 for  l  in os.listdir(PWDdir+"/patterns/"):
        l=l.strip()
        if not l.endswith(".cmd"):  continue
        li=l.replace('schema.site.','')
        N_PC=N_PC+1
        lines=[]
        ifile = open (PWDdir+"/patterns/"+l,'r')
        lines=lines+ifile.readlines()      # read file into list of lines
        ifile.close()
        for i in range(len(lines)):
                  xline=lines[i]
                  xline=xline.strip()
                  if xline.startswith("#"): continue

                  xline=xline.lower()
                  if xline.startswith("requirements"):
                     ii=xline.find("machine");
                     if ii>0:
                          xline=xline[ii+jj:len(xline)]
                          ii1=xline.find("\"");
                          xline=xline[ii1+1:len(xline)]

                          ii2=xline.find("\"");
                          xline=xline[0:ii2]
                          xline=xline.strip()
                          nodes.append(xline)
                          if (DEBUG): print "   --> data file name:",xline

 totCPU=0
 kk=1
 numCPU=[]
 for l in nodes:
    cmt="condor_status -format \"%30.30s:\" Name -format \"%10.10s\" State -format \"%10.10s\" Activity "+l
    f = os.popen(cmt, "r")
    num=0
    for s in f.xreadlines():
            s=s.strip()
            num=s.count(l)
            print "     -->"+str(kk)+" PC node="+l+" with="+str(num)+" cores found"
    numCPU.append(num)


# clear old database
 cmt  = 'rm -f '+ PWDdir+'/DataCollector/*.conf' 
 os.system( cmt )


 error=0
 DBases1=[]
 DBases2=[]
# discover database
 cmt="ls -t1 " + input
 f = os.popen(cmt, "r")
 kk=1 
 for s in f.xreadlines():
       s=s.strip()
       if not s.endswith(".gz"):  continue

       # check: does this box have database 
       ignore=0 
       sbox=""
       for box in nodes:
                if s.startswith(box): 
                               ignore=1 
                               sbox=box; 
       if (ignore == 0): continue
 

       if (kk>=N_PC): break;
       kk=kk+1
       DBases1.append(s)
       DBases2.append(sbox)
       if (DEBUG):
                print s


 if (kk != N_PC) :
            print "Failed to find recent database!"


 ifi=0
 for i in range (len(DBases1)):
       db=DBases1[i]
       ii=db.find(".")
       cpu=numCPU[i]
       if MaxJobsPerNode>0:
          cpu=MaxJobsPerNode    
       sname=DBases2[i]
       xbox=db[0:ii]
       cmt = 'zgrep \"'+partten+"\" "+input+db
       if (DEBUG):
                print "scan: "+xbox 

       tmpf="/tmp/"+sname+".conf"
       ifile = open (tmpf,'w')
       ifile.write("# Arcond configuration file from static data discovery\n")
       ifile.write("CPU_N="+str(cpu)+"\n")
       ifile.write("# Data stored: \n")
       f = os.popen(cmt, "r")
       kk=1
       for s in f.xreadlines():
         s=s.strip()
         kk=kk+1
         ifi=kk
         ifile.write(REDIRECTOR_NAME+s+"\n")
       ifile.close()
       cmt  = 'mv -f '+tmpf+" "+PWDdir+'/DataCollector/'
       os.system( cmt )
 
         # if (DEBUG):
                # print s

 if (ifi == 0) :
               return 1;

 return 0



