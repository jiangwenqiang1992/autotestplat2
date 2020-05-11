# coding=utf-8
from wicc.wiccrpc.box.RpcManager import RpcManager


class Wallet(object):
    """
    钱包即账号的集合，可以管理多个账号
    """

    @classmethod
    def encrypt_wallet(cls, password):
        """
        对钱包进行设置密码
        :return: 加密状态（true:加密成功，false:加密失败）
        """
        data = {
            "method": "encryptwallet",
            "params": [password]
        }
        return RpcManager.request(data)["result"]['encrypt']

    @classmethod
    def unlock_wallet(cls, password, second=3600):
        """
        解锁钱包，并设置解锁持续的时间
        :param password: 钱包密码
        :param second: 解锁持续的时间（秒），默认3600秒
        :return: 解锁状态（true:解锁成功、false:解锁失败）
        """
        data = {
            "method": "walletpassphrase",
            "params": [password, second]
        }
        return RpcManager.request(data)["result"]["passphrase"]

    @classmethod
    def lock_wallet(cls):
        """
        锁定钱包
        :return: rue:锁定成功, false:锁定失败
        """
        data = {
            "method": "walletlock",
            "params": []
        }
        return RpcManager.request(data)['result']['walletlock']

    @classmethod
    def update_wallet_password(cls, original_password, new_password):
        """
        更新钱包的加密密码
        :param original_password: 原密码
        :param new_password: 新密码
        :return: 更新状态 （true:修改成功、false:修改失败）
        """
        data = {
            "method": "walletpassphrasechange",
            "parames": [original_password, new_password]
        }
        return RpcManager.request(data)["result"]["chgpwd"]

    @classmethod
    def export_wallet(cls, path="./"):
        """
        导出钱包
        :param path: 到处的路径
        :return: （info 导出钱包的结果信息，key size：导出钱包中包含的地址账号数量）
        """
        data = {
            "method": "dumpwallet",
            "parames": [path]
        }
        result = RpcManager.request(data)["result"]
        return result['info'], result['key size']

    @classmethod
    def import_wallet(cls, path):
        """
        导入钱包
        :param path: 导入的路径
        :return: 导入的账号数量
        """
        data = {
            "method": "importwallet",
            "parames": [path]
        }
        return RpcManager.request(data)["result"]["imorpt key size"]

    @classmethod
    def backup_wallet(cls, path="./"):
        """
        备份钱包, 即备份wallet.dat文件
        :param path: 备份的路径
        :return:
        """
        data = {
            "method": "backupwallet",
            "parames": [path]
        }
        return RpcManager.request(data)["result"]

    @classmethod
    def wallet_info(cls):
        """
        获取钱包信息
        :return: 钱包信息
        """
        data = {
            "method": "getwalletinfo"
        }
        return RpcManager.request(data)['result']

