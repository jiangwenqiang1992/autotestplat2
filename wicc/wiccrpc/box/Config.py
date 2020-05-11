#!/usr/bin/python
# -*- coding: utf-8 -*-
from configparser import ConfigParser
import base64
import os


class Config(object):
    @classmethod
    def __content(cls):
        user = get_config("HOST", "username")
        password = get_config("HOST", "password")
        encode_str = "{}:{}".format(user, password).encode('utf-8')
        return "Basic " + base64.b64encode(encode_str).decode('utf-8')

    @classmethod
    def url(cls):
        return get_config("HOST", "host") + ":" + get_config("HOST", "port")

    @classmethod
    def header(cls):
        authorization = cls.__content()
        return {"Authorization": authorization, "content-Type": "application/json;"}


def get_config(tag, key, config="config.ini"):
    cf = ConfigParser()
    config_path = os.path.join(os.getcwd(), "")
    cf_path = os.path.join(config_path, config)
    cf.read(cf_path)
    return cf.get(tag, key)