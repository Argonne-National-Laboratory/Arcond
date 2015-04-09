#!/bin/bash
# S.Chekanov

# data set from the grid 
DATA="mc08.106070.PythiaZeeJet_Ptcut.recon.AOD.e352_s462_r541_tid025899" 

# specify download site 
SITE="MWT2_UC_MCDISK"


# directory where data set will be copied
DIR_TO_COPY="/tmp"

# hosts
names=( "atlas51"  "atlas52" "atlas53"  )
names_ext=".hep.anl.gov"

##############  DO NOT MODIFY BELOW ##########
#############################################
NSPLITS=${#names[@]}
echo "Number of splits=$NSPLITS"


date
echo "HOSTNAME is: " `hostname`
echo "The job starts at: " `date`

HOST=`hostname`

echo "Users online: "  `users` 
echo "CPU load: "  `uptime`

export AVERS=14.5.1
export TEST_AREA=$HOME/testarea
source /share/grid/app/asc_app/asc_rel/1.0/setup-script/set_atlas.sh


############ do in TMP directory for now #################
TMP="/tmp/arcond"
rm -rf $TMP
mkdir $TMP
cd $TMP

echo "Setting us arcond. Call arc_setup" 
arc_setup


################# determin stet 
SET=1
for (( i = 0 ; i < ${#names[@]} ; i++ ))
do
  HO=${names[$i]}$names_ext
  # echo $HO $HOST 
  if [ "$HO" = "$HOST" ]; then
     SET=$i
     echo "THIS IS HOST=$HO"
  fi
done

let "SET = $SET + 1"


echo "DATA SET=$SET will be copied"
############ make a file 
cat > $TMP/input.conf <<! 
#
data = $DATA
# how many splits
nsplits=$NSPLITS
# which set to get (0<=set<4)
get=$SET
# which remote site

# no specific site
# site=
site=$SITE
# site=BNL-OSG2_MCDISK
# site=MWT2_IU_MCDISK

# give the full path to the directory
# where to copy
dir=$DIR_TO_COPY
!
####################################


echo "Getting data. Call arc_get -allyes"
## Run
arc_get -allyes

echo "Checking:"
ls -la $DIR_TO_COPY/$DATA/ 
date
