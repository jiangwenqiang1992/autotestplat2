import json


def printJson(str):
    js = json.dumps(str, sort_keys=True, indent=4, separators=(',', ':'))
    print(js)