#! /bin/sh

echo "HELLO, ArCond!"
echo "HOSTNAME is: " `hostname`
echo "The job starts at: " `date`

echo "Users online: "  `users` 
echo "CPU load: "  `uptime`


echo "Show loaded data on local storage:"
ls -lt /data1/mc/PythiaZeegam25/aod 

# echo "2) Check data :"
# ls -lta /data1/chakanau 
# echo "3) Check space :" 
# df -h


