import datetime
import time

import requests
import json

def dingTalk(message):
    headers={
        "Content-Type": "application/json"
            }
    data={"msgtype": "text",
            "text": {
                 "content": message
            },
            "at": {
                "atMobiles": ["13267115656"]
            }
          }
    json_data=json.dumps(data)
    requests.post(url='https://oapi.dingtalk.com/robot/send?access_token=3db1db9c6e594cefa9944aebb6333e8bfee2db6c75f69ee9a589f57278ef86f7',data=json_data,headers=headers)
