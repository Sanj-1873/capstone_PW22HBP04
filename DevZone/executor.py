import subprocess
import threading
import uuid
import os
import json
from datetime import datetime,timedelta
import glob


class Executor:
    def __init__(self, template="DevZone/Terraform", logs="DevZone/DevLogs.txt"):
        self.temp_dir = template
        self.log_file = logs

    def deploy(self, tf_content):
        #returns .tf directory, list of instances
        tf_dir = os.path.join(self.temp_dir, uuid.uuid4().hex)
        os.mkdir(tf_dir)
        file_path = os.path.join(tf_dir,uuid.uuid4().hex+".tf")
        with open(self.log_file,"a") as log_fp:
                print(f"File stored as {file_path}")

        with open(file_path,"w") as tf_fp:
            print(tf_content,file=tf_fp)

        init_proc = subprocess.run(["terraform","init"],cwd = tf_dir, timeout=30)
        if init_proc.returncode:
            with open(self.log_file,"a") as log_fp:
                print(f"ERROR\tterraform init failed ({init_proc.returncode})",file=log_fp)
                return "",[]
        else:
            with open(self.log_file,"a") as log_fp:
                print(f"SUCCESS\tterraform init completed", file=log_fp)

        apply_proc = subprocess.run(["terraform","apply","-auto-approve"], cwd = tf_dir, timeout=90)
        if apply_proc.returncode:
            with open(self.log_file,"a") as log_fp:
                print(f"ERROR\tterraform apply failed ({apply_proc.returncode})",file=log_fp)
                self.destroy(tf_dir)
                return "",[]
        else:
            with open(self.log_file,"a") as log_fp:
                print(f"SUCCESS\tterraform apply completed", file=log_fp)

        ids = list()
        with open(os.path.join(tf_dir,"terraform.tfstate")) as state_file:
            state = json.load(state_file)
            for i in range(len(state["resources"])):
                for j in range(len(state["resources"][i]["instances"])):
                    ids.append(state["resources"][i]["instances"][j]["attributes"]["id"])
        tag_proc = subprocess.run(["aws", "ec2", "create-tags","--resources"," ".join(ids), "--tags", "Key=DevZone,Value=True"])
        return tf_dir,ids

    def stop(self, ids):
        #returns error code
        stop_proc = subprocess.run(["aws", "ec2", "stop-instances", "--instance-ids", " ".join(ids)])
        if stop_proc.returncode:
            with open(self.log_file,"a") as log_fp:
                print(f"ERROR\ttfailed to stop instances {ids} ({stop_proc.returncode})",file=log_fp)
                return stop_proc.returncode
        else:
            with open(self.log_file,"a") as log_fp:
                print(f"SUCCESS\tinstance was stopped", file=log_fp)
        return 0

    def start(self, ids):
        #returns error code
        stop_proc = subprocess.run(["aws", "ec2", "start-instances", "--instance-ids", " ".join(ids)])
        if stop_proc.returncode:
            with open(self.log_file,"a") as log_fp:
                print(f"ERROR\ttfailed to stop instances {ids} ({stop_proc.returncode})",file=log_fp)
                return stop_proc.returncode
        else:
            with open(self.log_file,"a") as log_fp:
                print(f"SUCCESS\tinstance was stopped", file=log_fp)
        return 0

    def destroy(self, tf_dir=None):
        #returns error code
        destroy_proc = subprocess.run(["terraform","destroy","-auto-approve"], cwd = tf_dir, timeout=60)
        if destroy_proc.returncode:
            with open(self.log_file,"a") as log_fp:
                print(f"ERROR\tfailed to clean up resources ({destroy_proc.returncode}). Please terminate resources manually",file=log_fp)
            return destroy_proc.returncode
        else:
            with open(self.log_file,"a") as log_fp:
                print(f"SUCCESS\tresources were destroyed", file=log_fp)
            return 0
    
    def probe(self, id, threshold, action):
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%dT%H:%M:00")
        probe_proc = subprocess.run(['aws', 'cloudwatch', 'get-metric-statistics', '--namespace', 'AWS/EC2', '--metric-name', 'CPUUtilization', '--period', '3600', '--statistics', 'Maximum', '--dimensions', f'Name=InstanceId,Value={id}', '--start-time', '2016-10-18T23:18:00', '--end-time', '2016-10-19T23:18:00'], timeout = 120, capture_output=True)
        if probe_proc.returncode:
            with open(self.log_file,"a") as log_fp:
                print(f"ERROR\tfailed to get metrics from resource ({probe_proc.returncode}). Please terminate resources manually",file=log_fp)
            return probe_proc.returncode
        else:
            output = json.loads(probe_proc.stdout)
            if len(output["Datapoints"]):
                for point in output["Datapoints"]:
                    if point["Maximum"]>threshold:
                        return
            if action == "stop":
                self.stop([id])
            else:
                states = glob.glob(os.path.join("DevZone/Terraform/","*/*.tfstate"))
                for state_file in states:
                    with open(state_file) as tf_state:
                        tf_data = json.load(tf_state)
                        try:
                            if tf_data['resources'][0]['instances'][0]['attributes']['id'] == id:
                                p = Path(state_file)
                                self.executor.destroy(tp.parent)
                        except:
                            continue

if __name__ == "__main__":
    e = Executor()
    contents = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    filepath, ids = e.deploy("\n".join(contents))
    e.stop([ids[0]])
    e.destroy(filepath)