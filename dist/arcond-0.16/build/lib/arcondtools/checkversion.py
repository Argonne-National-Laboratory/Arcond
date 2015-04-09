# Arcond v1.0
# S.Chekanov (ANL)

import os,sys
import glob
import time



# check arcond version
def checkversion(term, PWD, DEBUG): 
 
 if (DEBUG): print "---> Checking ArCond version"



 Err=0;
 file_master="/users/condor/Arcond/admin/version.txt"
 try:
      about = os.stat(file_master)
      if (about<1):
         if (DEBUG==True) : print "checkversion says:  Corrupted file: ",file_master 
         return Err 
 except OSError:
         if (DEBUG==True) : print "checkversion says:  Not found: ",file_master 
         return Err 



 file_local= PWD+"/admin/version.txt"
 try:
      about = os.stat(file_local)
      if (about<1):
           if (DEBUG==True) : print "checkversion says:  Corrupted file: ",file_local 
           return Err 
 except OSError:
       if (DEBUG==True) : print "checkversion says:  Not found: ",file_local 
 

 if (DEBUG==True) :
        print "Found master=",file_master
        print "Found local=",file_local 
  

 lines=[]
 ifile = open (file_master,'r')
 lines=lines+ifile.readlines()      # read file into list of lines
 ifile.close()
 master=0
 for i in range(len(lines)):
                  xline=lines[i]
                  xline=xline.strip()
                  if xline.startswith("#"): continue
                  master=int(xline)
                  break
   

 lines=[]
 ifile = open (file_local,'r')
 lines=lines+ifile.readlines()      # read file into list of lines
 ifile.close()
 local=0
 for i in range(len(lines)):
                  xline=lines[i]
                  xline=xline.strip()
                  if xline.startswith("#"): continue
                  local=int(xline)
                  break


 if (DEBUG==True) : 
      print "Compare timestamps:"
      print "   Master timestamp=",master
      print "     User timestamp=",local

 # generate error
 if (master>local) :
            Err=1
            return Err 
 
 return Err
