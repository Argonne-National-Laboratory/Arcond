# part of ArCond v1
# S.Chekanov (ANL)


import os,sys,shutil
import glob
import time


def duplicates(term,DIR): 
 
 print "---> Checking for duplicate input data files"

 REDO=False
# initial processing:
 COMM=[]
 NAME=[]
 DATA=[]
 dataDIC={}
 for  l  in os.listdir(DIR):
        l=l.strip()
        if not l.endswith(".conf"):  continue
        lines=[]
        ifile = open (DIR+l,'r')
        lines=lines+ifile.readlines()      # read file into list of lines
        ifile.close()
        comm=[]
        data=[]
        for i in range(len(lines)):
                  xline=lines[i]
                  xline=xline.strip()
                  ii=xline.find("CPU_N");
                  if xline.startswith("#") or ii>-1:
                          comm.append(xline)
                  else: 
                          data.append(xline)
                          if (dataDIC.has_key( xline )):
                                      print term.render('${YELLOW}WARNING: Dublicate data file is found!${NORMAL}')
                                      print "  --> data file name:",xline
                                      print "  --> found in the configuration file:", DIR+l
                                      print "  --> this file will be removed from this configuration file!"
                                      REDO=True
                          try:
                            dataDIC[xline]=l                     
                          except KeyError:
                                print term.render('${RED}Key error!${NORMAL}')
                        	print "  --> BAD KEY VALUE=", xline	
                                
        COMM.append(comm)
        NAME.append(l)
        DATA.append(data)
        del comm
        del data


# calculate the total number of input files:
 ntot=0
 for i in range(len(DATA)):
            xda=DATA[i]
            n_files=len(xda)
            conf=NAME[i].replace('.conf','')
            print '    --> PC node=',conf,'  has ',n_files, ' input files'
            ntot=ntot+n_files
 print '    --> ## SUMMARY: Total number of input files =',ntot 



# rebuild data assuming unique file names
 if (REDO):
    print "Removing duplicate input files and redo configuration files.." 
    del DATA
    DATA=[]
    for m in NAME:
      data=[]
      for k, v in dataDIC.iteritems():
          # print k, v
          if  (v == m): data.append(k) 
      data.sort()
      DATA.append(data) 
      del data 

 if (REDO):
  ntot=0
  for i in range(len(DATA)):
            xda=DATA[i]
            n_files=len(xda)
            ntot=ntot+n_files
  print '    --> ## SUMMARY: Total number of files for actual calculations =',ntot    




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
          
