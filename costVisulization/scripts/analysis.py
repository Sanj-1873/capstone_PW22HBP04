import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

#Getting Global Data 

region=["us-east-1", "us-east-2", "us-west-1", "us-west-2", "ap-south-1", "ap-northeast-3", "ap-northeast-2", "ap-southeast-1", "ap-southeast-2", "ap-northeast-1", "ca-central-1", "eu-central-1", "eu-west-1", "eu-west-2", "eu-west-3", "eu-north-1", "sa-east-1"]
data_globally = pd.DataFrame()
for region_name in region:
    df = pd.read_csv("data/region-"+ region_name +".csv")
    data_globally = pd.concat([df, data_globally])

data_globally = data_globally.rename(columns = {'instance': 'instanceid'}, inplace = False)
data_globally.to_csv("global/global_data.csv")


#create global views
y = data_globally.groupby('region').count()
ec2_distribution = y["id"]
if ec2_distribution.empty:
    pass
else:
    ec2_distribution.plot.bar()
    plt.savefig('graphs/global_view.png')


regions = data_globally['region'].unique()
df_names = []
for region in regions:
    region = region.replace("-","_")
    df_names.append('ec2_stats_'+region)
print(df_names)


#Merging data together to create regional information
for region in regions:
    cpu = pd.read_csv("data/region-"+region +"-cpuutilization.csv")
    #print(cpu.head())
    network_in = pd.read_csv("data/region-"+region+"-networkin.csv")
    #print(network_in.head())
    network_out = pd.read_csv("data/region-"+region+"-networkout.csv")
    #print(network_out.head())
    network = network_in.join(network_out.set_index('instanceid'),on='instanceid',how='outer')
    ec2_stats = network.join(cpu.set_index('instanceid'),on='instanceid',how='outer')
    ec2_stats = ec2_stats.join(data_globally.set_index('instanceid'),on='instanceid',how='inner')
    
    name = region.replace("-","_")
    def determine_state(ec2_stats, cid):
        state = []
        for i in range(len(cid)):
            if((ec2_stats[" cpuutilization%"][i] < 1) and (ec2_stats[" networkoutGiB"][i] < 1) and (ec2_stats[" networkinGiB"][i] < 1)):
        #print(ec2_stats["networkinGiB"])
                state.append('idle')
            else:
                state.append('active')
        return state

    determine_state(ec2_stats, ec2_stats["instanceid"])
    ec2_stats = ec2_stats.assign(state = determine_state(ec2_stats, ec2_stats["instanceid"]) )
    
    
    ec2_stats.to_csv("region_stats/ec2_stats_"+name+".csv")
    #print(ec2_stats["cpuutilization%"])