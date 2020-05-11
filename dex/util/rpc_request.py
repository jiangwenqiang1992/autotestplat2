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
    height = rpc.call('getinfo', [])[0]['synblock_height']
    #result = rpc.call('getaccountinfo', ['wNDue1jHcgRSioSDL4o1AzXz3D72gCMkP6'])
    # result = rpc.call('submitdexselllimitordertx', ['wNDue1jHcgRSioSDL4o1AzXz3D72gCMkP6', 'WUSD', 'XT:2:wi', 100000000, 0])
    # print(json.dumps(result, indent=2))
    # result = rpc.call('gettxdetail', ['2ca378f15ede51d7c952de3d646ffd11f7d424b76b3035a8ef412bc098451d87'])
    #print(response[0]["error"])
    #print(json.dumps(result, indent=2))
    rawtx = '540199de4e020002045749434383e1ac000457555344025854a49faec700858c20463044022063fa0bdcd68f080fbae6a7b650329a46d31c669f2f215ebecc9f2b6d70f3483f02200262b12b895400ec2fcdf7aa9a0098f4f74a572a7fd07a11efe2ce8a77e064a1'
    result = rpc.call('submittxraw', [rawtx])
    print(json.dumps(result, indent=2))



