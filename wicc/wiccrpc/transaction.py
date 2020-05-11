# coding=utf-8
from wicc.wiccrpc.box.RpcManager import RpcManager


class Transaction(object):

    @classmethod
    def transfer(cls, sender, receiver, amount, fee=10000):
        """
        从源地址账户转账到目的地址账户，手续费默认为:10000sawi
        :param sender: 发送者地址
        :param receiver: 接受者地址
        :param amount: 发送金额(单位sawi)
        :param fee: 交易费用(单位sawi),最少10000sawi
        :return: 交易Hash
        """
        data = {
            "method": "sendtoaddresswithfee",
            "params": [sender, receiver, amount, fee]
        }
        return RpcManager.request(data)['result']['hash']

    @classmethod
    def generate_signature(cls, sender, receiver, amount, fee=10000):
        """
         生成交易签名
        :param sender: 发送者地址
        :param receiver: 接受者地址
        :param amount: 发送金额(单位sawi)
        :param fee: 交易费用(单位sawi),最少10000sawi
        :return: 交易签名
        """
        data = {
            "method": "gensendtoaddresstxraw",
            "params": [fee, amount, sender, receiver]
        }
        return RpcManager.request(data)['result']['rawtx']

    @classmethod
    def submit_signature(cls, signature):
        """
        提交交易至区块链
        :param signature: 已创建的交易签名字段，通过generate_signature生成
        :return: 交易哈希
        """
        data = {
            "method": "submittx",
            "params": [signature]
        }
        return RpcManager.request(data)['result']['hash']

    @classmethod
    def transaction_info(cls, txhash):
        """
        交易哈希查询交易详情
        :param txhash: 交易的Hash
        :return: 交易详情
        """
        data = {
            "method": "gettxdetail",
            "params": [txhash]
        }
        return RpcManager.request(data)['result']

    @classmethod
    def current_transaction_hash_list(cls):
        """
        获取当前节点交易Hash列表
        :return: ConfirmTx: 已确认的交易哈希列表, UnConfirmTx 未确认的交易哈希列表
        """
        data = {
            "method": "listtx"
        }
        return RpcManager.request(data)['result']

    @classmethod
    def current_unconfirmed_transaction_list(cls):
        """
        获取当前节点未被确认的交易列表
        :return: 当前节点未被确认的交易列表
        """
        data = {
            "method": "listunconfirmedtx"
        }
        return RpcManager.request(data)['result']["UnConfirmTx"]

    @classmethod
    def current_all_transaction_list(cls, count):
        """
        获取当前节点交易详情
        :param count: 条数
        :return: UnConfirmed & Confirmed
        """
        data = {
            "method": "getalltxinfo",
            "params": count
        }
        return RpcManager.request(data)['result']

    @classmethod
    def decode_transaction_info(cls, hexstring):
        """
        获取交易详情
        :param hexstring: 条数
        :return: UnConfirmed & Confirmed
        """
        data = {
            "method": "getalltxinfo"
        }
        return RpcManager.request(data)['result']


if __name__ == '__main__':
    Transaction.all_transfer_list(10)
