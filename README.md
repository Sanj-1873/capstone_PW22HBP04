# Syneffo - An AWS Cloud Visualiser
## There are 2 parts in this project, the cost visulization and the devZone

### Steps to run the costVisulization. 
1. PreReq: Aws secret key and access key
2. To configure the aws keys, 
`aws configure`

`cd costVisulization/
chmod +x s_main.sh
./s_main.sh`

To build the docker image, past the keys in the Dockerfile 

`docker build .`

### Steps to run the DevZone
Prereq: AWS CLI must be configured, Terraform.

To deploy instances, SCP your terraform templates and rules into the folders `DevZone/Templates` and `DevZone/RuleList/Rules` respectively. Then run `/DevZone/daemon.py`. 
It will automatically discover the templates and rules to deploy and monitor the instances. 