#!/bin/bash
 
DAY= date --iso-8601 | tr -d '\n'
START_TIME=${DAY}T00:00:00.000Z
END_TIME=${DAY}T23:59:59.000Z
#echo ${START_TIME}
echo ${END_TIME}

# echo "instanceid, networkout(GiB)" > networkout.csv
# echo "Network Out"
# ./network_usage.sh us-east-1 NetworkOut 2021-08-10T00:00:00.000Z 2021-08-10T23:59:59.000Z  >> networkout.csv

# echo "instanceid, networkin(GiB)" > networkin.csv
# echo "Network In"
# ./network_usage.sh us-east-1 NetworkIn 2021-08-10T00:00:00.000Z 2021-08-10T23:59:59.000Z  >> networkin.csv

# echo "instanceid, cpuutilization(%)" > cpuutilization.csv
# echo "CPU Utilization"
# ./cpu_usage.sh us-east-1 CPUUtilization 2021-08-10T00:00:00.000Z 2021-08-10T23:59:59.000Z  >> cpuutilization.csv