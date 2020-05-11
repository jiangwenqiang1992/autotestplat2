
from wicc.wiccrpc.box.RpcManager import RpcManager


class Account(object):

    @classmethod
    def list(cls):
        """
        查询当前节点地址列表信息
        :return: 返回地址列表
        """
        data = {
            "method": "listaddr",
            "params": []
        }
        return RpcManager.request(data)["result"]

    @classmethod
    def generate_account(cls):
        """
        创建新地址
        :return: 新地址
        """
        data = {
            "method": "getnewaddress"
        }
        return RpcManager.request(data)["result"]["addr"]

    @classmethod
    def register_account(cls, address, fee=10001):
        """
        激活账户,新建的地址必须激活后才能作为交易发起方
        :param address:  需要激活的地址
        :param fee: 激活使用的小费 (单位sawi)
        :return: 激活的交易Hash
        """
        data = {
            "method": "registeraccounttx",
            "params": [address, fee]
        }
        return RpcManager.request(data)["result"]

    @classmethod
    def account_info(cls, address):
        """
        获取普通账户/合约账户地址详情
        :return: 账号信息
        """
        data = {
            "method": "getaccountinfo",
            "params": [address]
        }
        return RpcManager.request(data)["result"]

    @classmethod
    def get_private_key(cls, address):
        """
        获取地址对应的私钥
        :param address: 本钱包里普通账户地址
        :return:  私钥(WIF格式）
        """
        data = {
            "method": "dumpprivkey",
            "params": [address]
        }
        return RpcManager.request(data) #["privkey"]

    @classmethod
    def import_private_key(cls, private_key):
        """
        将私钥（由private key导出）导入钱包
        :param private_key: 普通账户地址私钥（WIF格式）
        :return: 普通账户地址
        """
        data = {
            "method": "importprivkey",
            "params": [private_key]
        }
        return RpcManager.request(data)["result"]

    @classmethod
    def validate_address(cls, address):
        """
        检查普通地址或者合约地址是否有效
        :param address:  普通账户/合约账户的地址/regid
        :return:
        """
        data = {
            "method": "validateaddr",
            "params": [address]
        }
        return RpcManager.request(data)["result"]["ret"]
