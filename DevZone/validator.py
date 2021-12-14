import json, glob, jsonschema, os

from jsonschema import validate

log_path = "DevZone/DevLogs.txt"

class Rules:
    def __init__(self, schema_path = "DevZone/RuleList/rules.schema.json", rules_folder = "DevZone/RuleList/Rules"):
        self.schema_path = schema_path
        self.rules_folder = rules_folder
        self.rules = dict()
        self.globals = list()
        with open(schema_path) as schema_fp:
            self.schema = json.load(schema_fp)
    
    def validate_file(self,filepath):
        try:
            with open(filepath) as fp:
                json_data = json.load(fp)
                validate(json_data, self.schema)
                if json_data["ruleId"] in self.rules.keys():
                    ruleId = str(json_data["ruleId"])
                    raise ValueError("Rule with ID "+ruleId+" already exists.")
                elif json_data["templateURI"]:
                    self.rules[json_data["templateURI"]] = json_data
                else:
                    self.globals.append(json_data)
        except Exception as err:
            with open(log_path,"a") as logs:
                print(f"ERROR\tCould not validate rule\n\t\t{err}", file=logs)
        else:
            with open(log_path,"a") as logs:
                ruleId = json_data["ruleId"]
                print(f"SUCCESS\tRule {ruleId} validated", file=logs)

    def validate_all(self):
        with open(log_path,"a") as logs:
            print(f"Validating all files in \'{self.rules_folder}\'", file=logs)
        files = glob.glob(os.path.join(self.rules_folder,"*.json"))
        for json_file in files:
            self.validate_file(json_file)
                
if __name__ == "__main__":
    v = Rules()
    v.validate_all()