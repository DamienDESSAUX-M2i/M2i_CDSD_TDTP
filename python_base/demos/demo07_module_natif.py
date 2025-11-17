import csv
import json

with open("demos/csv_file.csv", "wt", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(["nom", "prenom", "age"])
    csv_writer.writerow(["tata", "toto", "12"])

with open("demos/csv_file.csv", "rt", newline="", encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        print(row)

with open("demos/json_file.json", "w") as json_file:
    my_dict = {
        "nom": "tata",
        "prenom": "toto",
        "age": 5
    }
    json.dump(my_dict, json_file, indent=4)

with open("demos/json_file.json", "r") as json_file:
    my_dict = json.load(json_file)
    print(my_dict)
    my_str = json.dumps(json_file)
    print(my_str)