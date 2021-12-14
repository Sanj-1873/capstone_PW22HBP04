import schedule, time, subprocess, threading, json, glob, os
from validator import Rules
from executor import Executor
from pathlib import Path

class Daemon:
    def __init__(self, log_path = "DevZone/DevLogs.txt"):
        self.validator = Rules()
        self.executor = Executor()
        self.validator.validate_all()
        self.id_map = dict()

        for file_path in self.validator.rules:
            with open(file_path) as fp:
                tf_path, ids = self.executor.deploy(fp.read())
                for id in ids:
                    self.id_map[id] = self.validator.rules[file_path]

    def run(self):
        for id in self.id_map.keys():
            if "timeRule" in self.id_map[id].keys():
                if self.id_map[id]["action"] == "stop":
                    schedule.every().day.at(self.id_map[id]["timeRule"]["start"]).do(self.executor.stop, ids=[id])
                else:
                    states = glob.glob(os.path.join("DevZone/Terraform/","*/*.tfstate"))
                    for state_file in states:
                        with open(state_file) as tf_state:
                            tf_data = json.load(tf_state)
                            try:
                                if tf_data['resources'][0]['instances'][0]['attributes']['id'] == id:
                                    p = Path(state_file)
                                    schedule.every().day.at(self.id_map[id]["timeRule"]["start"]).do(self.executor.destroy, tf_dir = str(p.parent))
                            except:
                                continue
            if "usageRule" in self.id_map[id].keys():
                schedule.every(5).minutes.do(self.executor.probe, id=id, threshold=self.id_map[id]["usageRule"]["minimumCPU"], action=self.id_map[id]["action"])
        print("Scheduling done!")
        while True:
            schedule.run_pending()
            time.sleep(1)



if __name__ == "__main__":
    d = Daemon()
    d.run()