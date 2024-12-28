import csv
import json

DATAFILE = './test-data/trainingdata.jsonl'
DATAFILE_CSV = './test-data/trainingdata.csv'
DATAFILE_FT = './test-data/trainingdata_ft.jsonl'
DATAFILE_FT_CSV= './test-data/trainingdata_ft.csv'

SRC_FILE = './test-data/trainingdata_rag.txt'


def createSet(sys:str, user:str, model:str):
    if sys == '':
        full_set = {
            "messages": [
                { 
                    "role": "user", 
                    "content": user 
                },
                {   
                    "role": "model", 
                    "content": model 
                }
            ]
        }
        return full_set
    
    full_set = {
        "messages": [
            {
              "role": "system",
                   "content": sys
             },
             { 
                "role": "user", 
                "content": user 
              },
               {   
                "role": "model", 
                 "content": model 
             }
         ]
       }
    return full_set

def createFTSet(input: str, action: str, output: str):
    set = {'input': input,'action': action, 'output': output}
    return json.dumps(set, ensure_ascii=False)
    
def writeFTSetToFile(set: str):
    with open(DATAFILE_FT, 'a') as file:
        file.write(set + '\n')
    

def writeSetToFile(set, file):
    writer = open(file, 'a')
    set_to_str = ''
    writer.write(json.dumps(set, ensure_ascii=False) + "\n")
    writer.close()
    writer = open('./test-data/trainingdata-backup.jsonl', 'a')
    writer.write(json.dumps(set, ensure_ascii=False) + "\n")
    writer.close()

def convertTxtToJSONL(src, target):
    reader = open(src, 'r')
    lines = reader.readlines()
    sys = ''
    user = ''
    model = ''
    for line in lines:
        role = line[0]
        if role == 'S':
            sys = line.split('S: ', 1)[1]
        if role == 'U':
            user = line.split('U: ', 1)[1][:-1]
        if role == 'M':
            model = line.split('M: ', 1)[1][:-1]
        if user != '' and model != '':
            full_set = createSet(sys, user, model)
            writeSetToFile(full_set, target)
            user = ''
            model = ''

def convertTxtToCSV(src, target):
    reader = open(src, 'r')
    lines = reader.readlines()
    writer = csv.writer(open(target, 'w'))
    writer.writerow(['user', 'model'])
    user = ''
    model = ''
    for line in lines:
        role = line[0]
        if role == 'U':
            user = line.split('U: ', 1)[1][:-1]
        if role == 'M':
            model = line.split('M: ', 1)[1][:-1]
            if (len(model) >= 4000):
                model = model[:4000]
        if user != '' and model != '':
            writer.writerow([user, model])
            user = ''
            model = ''
    
def convertFTSetsToCSV():
    with open(DATAFILE_FT_CSV, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['input', 'output'])
        reader = open(DATAFILE_FT, 'r')
        lines = reader.readlines()
        for line in lines:
            line_js = json.loads(line)
            input = line_js['input']
            action = True if line_js['action'] == 'True' else False
            output = {
                "action": action,
                "params": line_js['output']
            }
            output_json = json.dumps(output)
            writer.writerow([input, output_json])


    
def clearFile(file:str):
        open(file, 'w').close()
