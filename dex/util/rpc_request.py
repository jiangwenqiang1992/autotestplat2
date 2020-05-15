import random

import requests
import json
import base64

class WiccRPC(object):
    def __init__(self, host, username, password):
        self.username = username
        self.password = password
        self.host = host
        bytesString = (username + ":" + password).encode(encoding='utf-8')
        token = base64.b64encode(bytesString)
        self.headers = {'content-type': 'application/json',
                        'Authorization': 'Basic ' + token.decode('utf-8'),
                        'Connection': 'close'}

    def call(self,  methodname, params):
        payloads = [{
            "method": methodname,
            'params': params,
            'jsonrpc': '2.0',
            'id': 'curltext'
        }]
        response = requests.post(url=self.host, data=json.dumps(payloads), headers=self.headers)
        if response.status_code == 200:
            return response.json()[0]['result'], response.json()[0]['error']
        else:
            print('RPC call failed, error is ', response.status_code)


if __name__ == '__main__':
    rpc = WiccRPC('http://10.0.0.31:6968', 'wayki', 'admin@123')
    #height = rpc.call('getinfo', [])[0]['synblock_height']
    #result = rpc.call('getaccountinfo', ['wPp4M2KJVLE85ubvJ8iTAywu3QcJy7d4aR'])
    #result = rpc.call('submitdexselllimitordertx', ['wNDue1jHcgRSioSDL4o1AzXz3D72gCMkP6', 'WICC', 'XT:45:wi', 40000000, 0])

    # for i in range(100):
    #     price = random.randrange(40000000, 50000000)
    #     amount = random.randrange(40000000, 50000000)
    #     result = rpc.call('submitdexbuylimitordertx',
    #                   ['wNDue1jHcgRSioSDL4o1AzXz3D72gCMkP6', 'WICC', 'XT:{}:sawi'.format(amount), price, 0])
    #     print(json.dumps(result, indent=2))
    # print(json.dumps(result, indent=2))
    result = rpc.call('gettxdetail', ['5b9a470e4445b83e9460771cb7f520c5511261782bbe1724a053bf27efceb8c1'])
    #result = rpc.call('getdexorder', ['05ee75fd0bd46843e29a1e5d8b4c45301178fe568bfe654bf5bcdcccaef24884'])
    #print(response[0]["error"])
    #print(json.dumps(result, indent=2))
    #rawtx = '540199de4e020002045749434383e1ac000457555344025854a49faec700858c20463044022063fa0bdcd68f080fbae6a7b650329a46d31c669f2f215ebecc9f2b6d70f3483f02200262b12b895400ec2fcdf7aa9a0098f4f74a572a7fd07a11efe2ce8a77e064a1'
    #result = rpc.call('submittxraw', [rawtx])
    print(json.dumps(result, indent=2))



#5b9a470e4445b83e9460771cb7f520c5511261782bbe1724a053bf27efceb8c1  05ee75fd0bd46843e29a1e5d8b4c45301178fe568bfe654bf5bcdcccaef24884
