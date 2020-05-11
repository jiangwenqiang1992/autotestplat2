# coding=utf-8
from wicc.wiccrpc.box.RpcManager import RpcManager


class Block(object):

    @classmethod
    def current_height(cls):
        """
        获取当前节点区块高度
        :return: 高度值
        """
        data = {
            "method": "getblockcount"
        }
        return RpcManager.request(data)['result']

    @classmethod
    def block_hash(cls, height):
        """
        查询区块哈希值
        :param height: 区块高度
        :return: 区块哈希
        """
        data = {
            "method": "getblockhash",
            "params": [height]
        }
        return RpcManager.request(data)['result']['hash']

    @classmethod
    def block_info(cls, block):
        """
        获取区块信息
        :param block: 区块高度/区块哈希
        :return: 区块信息
        """
        data = {
            "method": "getblock",
            "params": [block]
        }
        return RpcManager.request(data)['result']

