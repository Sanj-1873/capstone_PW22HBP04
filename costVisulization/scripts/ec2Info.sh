#!/bin/bash

#DAY= date --iso-8601 | tr -d '\n'
DAY=2021-11-28
START_TIME=${DAY}T00:00:00.000Z
END_TIME=${DAY}T23:59:59.000Z

echo $(pwd)
INITIAL_WORKING_DIRECTORY=$(pwd)
region=("us-east-1" "us-east-2" "us-west-1" "us-west-2" "ap-south-1" "ap-northeast-3" "ap-northeast-2" "ap-southeast-1" "ap-southeast-2" "ap-northeast-1" "ca-central-1" "eu-central-1" "eu-west-1" "eu-west-2" "eu-west-3" "eu-north-1" "sa-east-1")


mkdir -p data

for i in ${region[*]}
do
	# echo "\"Region\":\"$i{" > data/region-$i.csv
	echo $i
	aws ec2 describe-instances --region=$i  --query="Reservations[*].Instances[*].{Instance:InstanceId,Subnet:SubnetId, InstanceType:InstanceType, LaunchTime:LaunchTime,StateCode:State.Code, StateName:State.Name, Tags:Tags }" --output json > data/region-$i.json
	
	echo "instanceid, networkoutGiB" >  data/region-$i-networkout.csv
	echo "Network Out"
	#./network_usage.sh $i NetworkOut 2021-08-10T00:00:00.000Z 2021-08-10T23:59:59.000Z  >> data/region-$i-networkout.csv
	./scripts/network_usage.sh $i NetworkOut ${START_TIME}  ${END_TIME}  >> data/region-$i-networkout.csv

	echo "instanceid, networkinGiB" >  data/region-$i-networkin.csv
	echo "Network In"
	#./network_usage.sh $i NetworkIn 2021-08-10T00:00:00.000Z 2021-08-10T23:59:59.000Z  >> data/region-$i-networkin.csv
	./scripts/network_usage.sh $i NetworkIn ${START_TIME}  ${END_TIME}  >> data/region-$i-networkin.csv

	echo "instanceid, cpuutilization%" >  data/region-$i-cpuutilization.csv
	echo "CPU Utilization"
	#./cpu_usage.sh $i CPUUtilization 2021-08-10T00:00:00.000Z 2021-08-10T23:59:59.000Z  >> data/region-$i-cpuutilization.csv
	./scripts/cpu_usage.sh $i CPUUtilization ${START_TIME}  ${END_TIME}  >> data/region-$i-cpuutilization.csv

done

# cat data/region-* > data/global.json