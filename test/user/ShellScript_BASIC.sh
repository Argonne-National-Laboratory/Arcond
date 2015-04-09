#!/bin/bash
# Created by S.Chekanov, ANL
#
echo '###### starting ARCOND JOB #############'
echo "ArCond: HOSTNAME is: " `hostname`
echo "ArCond: The job starts at: " `date`

ATLAS_RELEASE=XATHENAVERSIONX
SUBMISSION_DIR='XSUBMISSIONDIRX'
JobDIR='XXDIRXX'
PACKAGE_ROOT='XXPackageRootXX'
PACKAGE_NAME='XXPackageNameXX'


# --- Save current directory ---
CURR_DIR=`pwd`
echo "ArCond: Current dir=$CURR_DIR" 
echo "ArCond: Atlas Release : $ATLAS_RELEASE"
echo "ArCond: Package DIR : $SUBMISSION_DIR"
echo "ArCond: Submission DIR : $JobDIR"
echo "ArCond: Test enviroment variables:"
# echo "****************************************"
# echo "env | sort"
# echo "****************************************"
# env | sort
export USERNAME=`id -nu`

# time
TEST_ID=`date +%y-%m-%d-%H%M%S`
# look at all packages
# rpm -q -a | sort


echo "ArCond: USERNAME=$USERNAME"
echo "ArCond: setting env variables.."

########## prepare run dir #####################



TESTAREA_CONDOR=$CURR_DIR"/testarea"$TEST_ID
mkdir $TESTAREA_CONDOR
echo "ArCond: Check install area:"
ls -la  
mkdir $TESTAREA_CONDOR/$ATLAS_RELEASE
PACKDIR=$TESTAREA_CONDOR/$ATLAS_RELEASE"/"$PACKAGE_NAME 
TAR_PACKAGE=$PACKAGE_NAME".tgz"
RUNDIR=$TESTAREA_CONDOR/$ATLAS_RELEASE"/"$PACKAGE_NAME"/condor/"
mkdir $PACKDIR
mkdir $RUNDIR


echo "ArCond: copying the package starts at : " `date`
# go to release dir and copy package
cd  $TESTAREA_CONDOR/$ATLAS_RELEASE
cp  $SUBMISSION_DIR"/Job/"$TAR_PACKAGE  $TESTAREA_CONDOR/$ATLAS_RELEASE/$TAR_PACKAGE

echo "ArCond: untaring the package starts at : " `date`
tar -zvxf $TAR_PACKAGE
## package is ready


cd $PACKDIR/
echo "ArCond: List package directories in $PACKDIR"
ls -la * 



# sleep random number. Make sure that seed in jetphox is reset"
value=$RANDOM
t=`echo "scale=0; $value / 1000" | bc`
echo "ArCond= Sleep random number $t" 
sleep $t


# if ATLAS release is installed fron NFS/AFS
# setup it at random time (but within 1 min!)
# this is necessary for low-bandwidth Tier3 network
value=$RANDOM
t=`echo "scale=0; $value / 1000" | bc`
echo "ArCond= Sleep random number $t" 
sleep $t

# setup atlas release. Tier3 dependent 
export USER="condor_user"$TEST_ID
export AVERS=$ATLAS_RELEASE
export TEST_AREA=$TESTAREA_CONDOR
source /share/grid/app/asc_app/asc_rel/1.0/setup-script/set_atlas.sh

echo "ArCond: Compiling the package:"
cd $PACKDIR/cmt
 
cmt config; source setup.sh; make; 
# again for realeas 15.5 and above to fix user package
source setup.sh; make; 
ls -la



echo "ArCond: compilation finished at: " `date`

# echo "SC: Test enviroment variables:"
# echo "****************************************"
# echo "env | sort"
# echo "****************************************"
# env | sort

echo ""
USERNAME=`id -nu`

# time
TEST_ID=`hostname -f`-`date +%y-%m-%d-%H%M`
echo "ArCond: execution starts at: " `date`
echo "ArCond: CMTCONFIG = $CMTCONFIG"
echo "ArCond: show  CMTPATH=$CMTCONFIG"


# copy scripts necessary for running
cp -f ${JobDIR}/Analysis.py          $RUNDIR
cp -f ${JobDIR}/InputCollection.py   $RUNDIR
cp -f $SUBMISSION_DIR/LVL1Config.xml $RUNDIR


# go to run dir
cd $RUNDIR 
echo "ArCond: List all files in run directory:"
ls -la


# running over the data 
logfile="Analysis.log"
athena.py Analysis.py  > ${logfile} 2>&1
FStatusGood="StatusGood.txt"
grep 'INFO leaving with code 0:' ${logfile} > $FStatusGood


# check directory
if [ -d $JobDIR ]; then
   echo "ArCond: Copy output to the directory=$JobDIR" 
else
  echo "ArCond: Error: $JobDIR does not exist! Did you remove it without waiting for end of job?"
  echo "ArCond: EXITING"
  exit 1
fi

echo 'ArCond: Check created files:'
ls -alrt

echo "ArCond: The job ends at: " `date`
gzip *.log
echo "ArCond: Copy all output back to $JobDIR"
cp *.log.gz          $JobDIR/ 
cp *.root            $JobDIR/
cp Analysis.py       $JobDIR/ 
cp $FStatusGood      $JobDIR/
 
echo "ArCond: All output was copied"
