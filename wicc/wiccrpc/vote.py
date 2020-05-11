# coding=utf-8
from wicc.wiccrpc.box.RpcManager import RpcManager


class Vote(object):
    """
    钱包即账号的集合，可以管理多个账号
    """
    @classmethod
    def vote(cls, sender, receiver, ticket_amount, fee=10000):
        """
        投票，手续费默认为:10000sawi
        :param sender: 发送者地址
        :param receiver: 投票地址
        :param amount: 发送金额(单位sawi)
        :param fee: 交易费用(单位sawi),最少10000sawi
        :return: 交易Hash
        """
        data = {
            "method": "votedelegatetx",
            "params": [sender, [{"delegate": receiver, "votes": ticket_amount*100000000}], fee]
        }
        return RpcManager.request(data)


