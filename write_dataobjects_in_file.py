import requests
import json
import os
from dotenv import load_dotenv


# FETCHES DATAOBJECTS AND FORMAT IT TO SRC_FILES
def fetch_convert():

    load_dotenv()

    from dataset_creator import SRC_FILE

    tokenId = os.getenv('SETHUB_TOKENID')
    tokenKey = os.getenv('SETHUB_TOKENKEY')
    product = 'setHUB'

    # AUTHORIZATION
    url = 'https://admin.ah-oh.com/auth-api/token/auth/sign-in'

    headers = {
        'Content-Type': 'application/json'
    }

    payload = json.dumps({
        'tokenId': tokenId,
        'tokenKey': tokenKey,
        'product': product
    })

    response = requests.post(url, headers=headers, data=payload).text
    token = json.loads(response)['token']


    # GET DATAOBJECTS
    url = os.getenv('SETHUB_GET_DATAOBJECTS')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    payload = json.dumps({
        'query': 'FindDataObject object',
    })

    response = requests.get(url, headers=headers, data=payload).text
    data_objects = json.loads(response)

    write_dataobjects_to_file(data_objects, SRC_FILE)

def write_dataobjects_to_file(data_objects, file):

    open(file, 'w').close()
    writer = open(file, 'a')

    # set to avoid duplicate faq's
    duplicates = set()

    fa_pairs = []

    for data_object in data_objects:

        content = data_object['content']
        f_raw = content['headline_intro']
        print(f_raw)
        if not f_raw or f_raw in duplicates:
            continue
        a_raw = content['steps']
        if not a_raw:
            continue
        duplicates.add(f_raw)
        f_raw = filterText(f_raw)[:-1]
        f_end = f_raw.find('?')
        f = f_raw[:f_end+1]
        a = f_raw[f_end+1:] + filterText(a_raw)
        fa_pairs.append({"f": f, "a": a})

        faqs = content['faq']
        for faq in faqs:
            f = faq['text1']
            if not f or f in duplicates:
                continue
            a = faq['text2']
            if not a or "Handbuch" in a:
                continue
            duplicates.add(f)
            fa_pairs.append({"f": f, "a": a})

    for pair in fa_pairs:
        writer.write(filterText(pair['f']) + '\n')
        writer.write(filterText(pair['a']) + '\n\n')

    writer.close()
    duplicates.clear()

def filterText(text: str):
    start = text.find('<')
    end = text.find('>')
    if end == -1:
        return text
    cutted = (text[:start] + text[end+1:])
    cutted = cutted.replace('&nbsp;', ' ')
    cutted = cutted.replace('&amp;', '&')
    cutted = cutted.replace('\\"', '"')
    return filterText(cutted)