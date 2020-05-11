# coding=utf-8
from wicc.wiccrpc.box.RpcManager import RpcManager


class Node(object):

    @classmethod
    def chain_info(cls):
        """
        获取链相关信息
        :return: 高度值
        """
        data = {
            "method": "getblockchaininfo"
        }
        return RpcManager.request(data)['result']

    @classmethod
    def node_info(cls):
        """
        获取节点相关信息
        :return: 节点信息
        """
        data = {
            "method": "getinfo"
        }
        return RpcManager.request(data)['result']
