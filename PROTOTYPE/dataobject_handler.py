import json

test_list = []
FILE = "./PROTOTYPE/storage_dataobjects.txt"

def read_dataobjects():
    with open(FILE, "r") as file:
        lines = file.readlines()
        for line in lines:
            test_list.append(json.loads(line))

read_dataobjects()

def write_dataobject(dataobject):
    test_list.append(dataobject)
    with open(FILE, "a") as writer:
        object_to_json = json.dumps(dataobject, ensure_ascii=False)
        writer.write(object_to_json + "\n")

def get_names():
    names = []
    for item in test_list:
       names.append(item['name'])
    return names

def update_file():
    with open(FILE, "w") as writer:
        for item in test_list:
            object_to_json = json.dumps(item, ensure_ascii=False)
            writer.write(object_to_json + "\n")
