# Arcond v1.0
# S.Chekanov (ANL)

# Check available CPUs


import os,sys,shutil
import glob
import time




def checknodes(term,PWD,MaxJobsPerNode): 
 
 print "---> Checking computing cores"

 Err=0
 DEBUG=False
 nodes=[] 
 jj=len("machine")
 for  l  in os.listdir(PWD+"/patterns/"):
        l=l.strip()
        if not l.endswith(".cmd"):  continue
        lines=[]
        ifile = open (PWD+"/patterns/"+l,'r')
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

 nodes.sort()
 totCPU=0
 kk=1
 box_stat=[]
 box_name=[]
 for l in nodes:
       cmt="condor_status -format \"%30.30s:\" Name -format \"%10.10s\" State -format \"%10.10s\" Activity "+l
       f = os.popen(cmt, "r")
       num=0
       for s in f.xreadlines():
             s=s.strip()
             num=s.count(l) 
       if MaxJobsPerNode<0: 
          print "     -->"+str(kk)+" PC node="+l+" with="+str(num)+" cores found"     
       else:
          print "     -->"+str(kk)+" PC node="+l+" with="+str(num)+" cores found, but "+str(MaxJobsPerNode)+" is used"
       box_name.append(l)
       if (num<1): 
                 Err=1
                 print term.render('${RED}ERROR: PC node=\''+l+'\' has no any CPU cores! ${NORMAL}')
                 print term.render('${RED}     --> This usually means that this PC is not in Condor${NORMAL}')
                 print term.render('${RED}     --> SOLUTION: Remove the corresponding file from \'patterns\' directory${NORMAL}')
       if MaxJobsPerNode>0: 
                  num=MaxJobsPerNode
       box_stat.append(num)
       totCPU=totCPU+num
       kk=kk+1
    
 if Err<1: print "---> Total number of found cores=",totCPU 
 return box_name,box_stat,Err
