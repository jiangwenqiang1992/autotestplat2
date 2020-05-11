#!/usr/bin/python
# -*- coding: utf-8 -*-


import requests
import json
import demjson


class BaasManager(object):

    # 默认测试网
    __is_main_net = False
    __main_net_baas_url = "https://baas.wiccdev.org/v2/api"
    __test_net_baas_url = "https://baas-test.wiccdev.org/v2/api"

    @classmethod
    def set_net(cls, is_main_net=False):
        if isinstance(is_main_net, bool):
            cls.__is_main_net = is_main_net
        return cls

    @classmethod
    def __post(cls, uri, request):
        if cls.__is_main_net:
            url = cls.__main_net_baas_url + uri
        else:
            url = cls.__test_net_baas_url + uri
        header = {
            "Content-Type": "application/json"
        }
        request = json.dumps(request)
        resp = requests.post(url=url, data=request, headers=header)
        return demjson.decode(resp.text)

    @classmethod
    def get_valid_height(cls):
        uri = "/block/getblockcount"
        return cls.__post(uri, {})["data"]

    @classmethod
    def submit_tx(cls, tx):
        uri = "/transaction/sendrawtx"
        request = {
            "rawtx": tx
        }
        return cls.__post(uri, request)

    @classmethod
    def decode_raw_tx(cls):
        pass

    @classmethod
    def transaction_detail(cls):
        pass


    @classmethod
    def cdp_info(cls, id):
        pass

    @classmethod
    def stable_coin_info(cls):
        pass
