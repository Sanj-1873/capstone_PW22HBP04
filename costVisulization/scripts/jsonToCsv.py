import json
import csv

region=["us-east-1", "us-east-2", "us-west-1", "us-west-2", "ap-south-1", "ap-northeast-3", "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-northeast-1", "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", "eu-north-1", "sa-east-1"]
for region_name in region:
	
	#Open JSON file 
	with open("data/region-"+ region_name +".json") as json_file:
		data = json.loads(json_file.read())


	f = csv.writer(open("data/region-"+ region_name +".csv","w+"))

	f.writerow(["id", "account_id", "region", "instance","subnet","instancetype", "launchtime","statecode","statename","name"])

	# for i in data:
	# 	for j in i:
	# 		print(j["Tags"][0]["Value"])
	count_id = 1
	for i in data:
		for j in i:
			f.writerow([count_id,
						3,
						region_name,
				        j["Instance"],
						j["Subnet"],
						j["InstanceType"],
						j["LaunchTime"],
						j["StateCode"],
						j["StateName"],
						j["Tags"][0]["Value"]])

			count_id = count_id+1






