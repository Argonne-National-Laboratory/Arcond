#!/bin/bash

# Backups all files in given directories ($DirList)
# except those file names/directory names/wildcards


DIR=`pwd`

## Where to backup -apper level
BackupDir=$DIR'/Job/'


## What directory to backup
DirList=$1

# directory path 
DirPath=$2


# go to the rot directory
cd $DirPath


#BackupLog
Datalog=$DirList".log"
#BackupName
BackupName=$DirList".tgz"

## Verbosity for tar, you may even add other tar options
#Verbose=""
Verbose="-v --totals"

## Nice for log files
## Nice for log files
echo  "Input directory:  $DirList"
echo  "Output     file:  $BackupName"
echo  "Output log file:  $Datalog"
echo  "Put backup files to :  $BackupDir"
echo  "Backup file: $BackupDir$Datalog"
TIMES=`date`
echo  "Backup and gzip started at $TIMES ..wait .."

#
tar -cvzf  $BackupDir$BackupName   $Verbose --exclude='*.o' --exclude='*.info' --exclude='*-opt' --exclude='CVS*' --exclude='*.exe' --exclude='core'   --exclude='*~'  --exclude='fort*' --exclude='*.tup' --exclude='*.log'  --exclude='*.gz' --exclude='*.a' --exclude='*.ps' --exclude='*.eps' --exclude='*.rz' --exclude='*.root'  $DirList > $BackupDir$Datalog


echo
TIMES2=`date`
echo -n "tar finished at $TIMES2"

cd $DIR


