#!/bin/sh
# this is a submission script to get data on-fly


DIR_CURRENT=`pwd`
DEFAULTPATTERNDIR=$DIR_CURRENT/patterns
SCHEMA=$ARCOND_SYS/etc/arcond/share

# If no Atlas release version is set, use the deafult
AVERS=${AVERS:-$DEFAULTAVERS}

 
# If there is only one parameter passed, the job is assumed to be local

JobName=$1
if [ $# -eq 1 ]; then
  Site=local
else
  Site=$2
fi


########################################################
# Part Three:  Build scripts and condor cmd file       #
########################################################

# echo "DEBUG: Call to ${JobName}" 
awk '/^# GridJob/ { print $0 }' ${JobName}.sh  | sed 's/# GridJob //'   > IO.cmd



# Construct the job shell script using the JobName.sh 
# and the template in the local directory, if present, otherwise
# from the default patterns directory


# echo "DEBUG: Start SED1"
if [ -e $SCHEMA/schema.job.generic.sh ]; then
   sed 's/AVERSION/'${AVERS}'/' $SCHEMA/schema.job.generic.sh | sed '/#JOB_COMMANDS/r '${JobName}'.sh' > $DIR_CURRENT/schema.job.${JobName}'.sh'
else
   sed 's/AVERSION/'${AVERS}'/' ${SCHEMA}/schema.job.generic.sh | sed '/#JOB_COMMANDS/r '${JobName}'.sh' > $DIR_CURRENT/schema.job.${JobName}'.sh'
fi


# echo "DEBUG: Start SED2"
# Construct the cmd file using the IO.cmd and the template
# in the local directory, if present, otherwise from the
# default pattern directory

if [ -e $DIR_CURRENT/schema.site.${Site}.cmd ]; then
  sed 's/USERNAME/'${USER}'/' $DIR_CURRENT/schema.site.${Site}.cmd | cat - IO.cmd  > $DIR_CURRENT/Schema.job.${Site}.cmd
else
  sed 's/USERNAME/'${USER}'/' ${DEFAULTPATTERNDIR}/schema.site.${Site}.cmd | cat - IO.cmd > $DIR_CURRENT/Schema.job.${Site}.cmd
fi

echo '' >> $DIR_CURRENT/Schema.job.${Site}.cmd
echo 'queue' >> $DIR_CURRENT/Schema.job.${Site}.cmd

if [ -e IO.cmd ]; then
  /bin/rm IO.cmd
fi


########################################################
# Part Four: make and fill a directory for the job     #
########################################################

SERIES=${JobName}.${Site}
JobDir=`mktemp ${SERIES}.XXXXX`
#echo "DEBUG: Remove the file since we intend to make a directory!"
if [ -e ${JobDir} ]; then
  /bin/rm ${JobDir}
fi
mkdir $DIR_CURRENT/Job.${JobDir}

mv $DIR_CURRENT/Schema.job.${Site}.cmd    $DIR_CURRENT/Job.${JobDir}/schema.job.${Site}.cmd
mv $DIR_CURRENT/schema.job.${JobName}.sh  $DIR_CURRENT/Job.${JobDir}


# echo "DEBUG: cd to Job.$JobDir"
cd Job.$JobDir
JobTag=$JobDir

# echo "DEBUG: Start SED3"
sed "s/SCRIPT/job.$JobTag.sh/" schema.job.${Site}.cmd > job.${Site}.cmd
sed "s/_SITE/${Site}/" schema.job.${JobName}.sh > job.${JobTag}.sh


# echo "DEBUG: Submit the jobs"

# echo "DEBUG: file ready: job.${Site}.cmd" 

#################################
# Part Five: Submit the jobs    #
#################################

# Slow things down.  This avoids NFS hangs due to a side 
# effect of keeping the log file unlocked.

chmod 755 *
sleep 0.2s

condor_submit    job.${Site}.cmd

pwd
exit
