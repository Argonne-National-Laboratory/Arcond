#!/bin/bash
# S.Chekanov
# Main submit script to build a database

# Usage: databuilde.sh inputdir


DIR_CURRENT=`pwd`

rm -f  $DIR_CURRENT/sent.sh
rm -rf $DIR_CURRENT/Job.sent.*
rm -f  $DIR_CURRENT/DataCollector/*
  
echo "DIR_CURRENT=$DIR_CURRENT"

OLD='XXDIRXX'
NEW=$DIR_CURRENT

sed "s,$OLD,$NEW,g" < $ARCOND_SYS/bin/collect.sh > $DIR_CURRENT/tmp.sh 


OLD='XXINPUTXX'
NEW=$1
sed "s,$OLD,$NEW,g" < $DIR_CURRENT/tmp.sh > $DIR_CURRENT/sent.sh
rm -f  $DIR_CURRENT/tmp.sh

 

declare -a computers 
index=0

for filename in $DIR_CURRENT/patterns/*.cmd
do

  file=${filename#*/}
  file=${file#*.}
  file=${file#*.}
  file=$(basename "$file" .cmd)
  
  echo 'Found PC node: ' $file
  computers[${index}]=$file 
  let "index = $index + 1"
done

NN=${#computers[*]}
# echo "Number of nodes=$NN"

# Doing it with a "for" loop instead:
for i in "${computers[@]}"
do
    echo "Submitting to $i"
    $ARCOND_SYS/bin/submit_db.sh sent  $i 
done

# clear
rm -f $DIR_CURRENT/sent.sh


exit 0

