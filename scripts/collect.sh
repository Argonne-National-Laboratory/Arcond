#!/bin/bash

# Usage: collect.sh <inputdir>


# setup grid
OSG_KIT="/share/grid/wlcg-client"
source $OSG_KIT/setup.sh


SUBMIT_DIR='XXDIRXX'

HOST_PC=`hostname`
echo 'Starting MC production Job'
echo "The HOSTNAME is: " $HOST_PC
echo "The job starts at: " `date`
# --- Save current directory ---
CURR_DIR=`pwd`
echo "SC: Current dir=$CURR_DIR" 


# echo "****************************************"
# echo "env | sort"
# echo "****************************************"
# env | sort

export USERNAME=`id -nu`

# time
TEST_ID=`date +%y-%m-%d-%H%M%S`
echo "SC: Execution time=${TEST_ID}"

# the number of CPUs available on the machine:
PARALLELCPUS=$(grep -c "vendor_id" /proc/cpuinfo)
echo "Arcond: Number of CPU="$PARALLELCPUS


# look at all packages
# rpm -q -a | sort


echo "Arcond: USERNAME=$USERNAME"


DIR='XXINPUTXX' 
echo "Arcond: Check run directory":

CONF_FILE=$HOST_PC".conf"

echo "# Arcond configuration file" > $CONF_FILE
echo "CPU_N=$PARALLELCPUS" >> $CONF_FILE
echo "# Data stored:" >> $CONF_FILE 

# get list of files
find $DIR -size +5k -type f >> $CONF_FILE 


# for f in $DIR/*
# do
#   pos=`expr index "$f" \*`
#   int=0
#    if [ $pos -gt $int ] ; then
#      echo "No data is found" 
#   else
#      echo $f >> $CONF_FILE   
#   fi
# done


echo "Arcond: print all input files:"
cat $CONF_FILE

# get output
cp $CONF_FILE $SUBMIT_DIR"/DataCollector/"
   
