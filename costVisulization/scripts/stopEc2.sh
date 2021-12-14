#!/bin/bash
REGION="$1"
INSTANCES="$2"

#Limitation, can only snapshot one instance at a time.. 
echo "Creating snapshots"
aws ec2 create-snapshots  --instance-specification InstanceId=${INSTANCES}  --description "Instance snapshot" --region=${REGION}

echo "Stopping instances"
aws ec2 stop-instances --region=${REGION} --instance-ids ${INSTANCES} 