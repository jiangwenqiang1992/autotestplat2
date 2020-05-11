import requests
import demjson
import json

from wicc.wiccrpc.box import Config


class RpcManager(object):
    @classmethod
    def request(cls, parameters):
        parameters["jsonrpc"] = "2.0"
        parameters["id"] = "curltext"
        data = json.dumps(parameters)
        resp = requests.post(Config.url(), headers=Config.header(), data=data)
        return demjson.decode(resp.text)