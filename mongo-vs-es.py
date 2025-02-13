import json

with open("/Users/sahkumar/sheetstoTestRails/pythonProject1/es-users.json", "r") as fd:
    es_data = json.load(fd)

with open("/Users/sahkumar/sheetstoTestRails/pythonProject1/mongo-users.txt", "r") as fd:
    lines = fd.readlines()


for data in es_data:
    person_id = data['key']
    if person_id in lines:
        print("yes")
    else:
        print("no")
