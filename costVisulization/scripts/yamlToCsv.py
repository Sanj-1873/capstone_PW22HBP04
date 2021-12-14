import csv
import yaml

fieldnames = ['Instance', 'InstanceType', 'LaunchTime', 'StateCode', '']

with open('output.csv', 'w', newline='') as f_output:
    csv_output = csv.DictWriter(f_output, fieldnames=fieldnames)
    csv_output.writeheader()

    for filename in ['Test_Co_1.txt', 'Test_Co_2.txt']:
        with open(filename) as f_input:
            data = yaml.safe_load(f_input)

        name = data[0]['Name']

        for entry in data:
            key = next(iter(entry))

            if key.startswith('Note') or key.startswith('Comment'):
                row = {'Name' : name}

                for d in entry[key]:
                    for get in ['Author', 'Written', 'About', 'Body']:
                        try:
                            row[get] = d[get]
                        except KeyError as e:
                            pass

                csv_output.writerow(row)


