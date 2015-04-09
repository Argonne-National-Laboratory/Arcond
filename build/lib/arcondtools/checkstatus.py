# Arcond v1.0
# S.Chekanov (ANL)

# check condor status

import os




def checkstatus(term,PWD): 
 
 print "---> Checking claimed CPUs"

 totClaimed=0
 Err=0
 DEBUG=False
 cmt="condor_status -claimed"
 f = os.popen(cmt, "r")
 for s in f.xreadlines():
       s=s.strip()
       if (DEBUG):
                print s
       ii=s.find("slot");
       if ii>-1:
               totClaimed=totClaimed+1 
   

 if totClaimed>0:
                Err=totClaimed; 
 
 if Err<1: print "---> Total number of claimed CPU cores=",totClaimed 
 return Err
