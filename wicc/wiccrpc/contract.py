# coding=utf-8
from wicc.wiccrpc.box.RpcManager import RpcManager


class Contract(object):

    @classmethod
    def register_contract(cls, address, file_path, fee=110000000):
        """
        用于发布智能合约
        :param address: 发布智能合约者的地址
        :param file_path: 发布的智能合约文件路径+文件名
        :param fee: 发布智能合约所需费用 （一般至少110000000
        :return: 发布合约交易的哈希
        """
        data = {
            "method": "registercontracttx",
            "params": [address, file_path, fee]
        }
        return RpcManager.request(data)

    @classmethod
    def contract_regid(cls, contract_hash):
        """
        获取智能合约的regid
        :param contract_hash: 发布合约时的交易哈希
        :return: 该智能合约的regid
        """
        data = {
            "method": "getcontractregid",
            "params": [contract_hash]
        }
        return RpcManager.request(data)['result']

    @classmethod
    def contract_info(cls, contract_id):
        """
        获取智能合约信息
        :param contract_id: 智能合约 regid
        :return: 智能合约信息
        """
        data = {
            "method": "getcontractinfo",
            "params": [contract_id]
        }
        return RpcManager.request(data)

    @classmethod
    def contract_account_info(cls, contract_regid, user):
        """
        用户在智能合约中的相关信息
        :param contract_regid: 发布合约时的交易哈希
        :param user: 查询的用户地址/regid
        :return: 该智能合约的regid
        """
        data = {
            "method": "getcontractaccountinfo",
            "params": [contract_regid, user]
        }
        return RpcManager.request(data)['result']

    @classmethod
    def contract_data(cls, contract_regid, key):
        """
        获取智能合约相关原生数据信息
        :param contract_regid: 合约regid
        :param key: 智能合约数据的key值
        :return: 该智能合约数据
        """
        data = {
            "method": "getcontractdata",
            "params": [contract_regid, key]
        }
        return RpcManager.request(data)['result']

    @classmethod
    def call_contract(cls, user, contract_regid, contract_command, fee=1000000, amount=0,):
        """
        调用智能合约(合约必须是被确认状态)
        :param user: 合约调用者地址/regid
        :param contract_regid: 智能合约的regid
        :param amount: 向智能合约发送维基币的数量(sawi)
        :param contract_command: 调用合约的命令
        :param fee: 调用合约交易所需费用
        :return: 调用合约的交易哈希
        """
        data = {
            "method": "callcontracttx",
            "params": [user, contract_regid, amount, contract_command, fee]
        }
        return RpcManager.request(data)

    @classmethod
    def contract_list(cls, show_detail=False):
        """
        获取已发布的智能合约列表
        :param show_detail:
        :return:
        """
        data = {
            "method": "listcontracts",
            "params": [show_detail]
        }
        return RpcManager.request(data)['result']

