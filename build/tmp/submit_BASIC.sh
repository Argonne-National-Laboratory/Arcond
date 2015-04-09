#!/bin/bash
# submit script 


CURR_DIR=`pwd`


# to submit to some site 
SITE="XXsiteXX"

# what shell script to process
INPUT="ShellScript"


chmod 755 *	
# submitting
$CURR_DIR/submit_job.sh $INPUT $SITE


echo 'All is done'
exit 0
