#!/usr/bin/python
# -*- coding: utf-8 -*-

from wicc.transactions import *
from cryptos import *


def number_to_var_int(number):
    batch = 0
    num = number
    while True:
        batch += 1
        if num <= 0x7F:
            break
        num = (num >> 7) - 1

    tmp_list = [0 for _ in range(0, int((batch * 8 + 6) / 7))]
    index = 0
    while True:
        cache = 0
        if index == 0:
            cache = 0x00
        else:
            cache = 0x80
        tmp_list[index] = number & 0x7F | cache
        if number <= 0x7F:
            break
        number = (number >> 7) - 1
        index += 1
    return bytes(tmp_list[batch - 1::-1])


def number_str_to_bytes(str_):
    t = str_.upper()
    p = re.compile('.{1,2}')
    return bytes([int(x, 16) for x in p.findall(t)])


class Serializer(object):
    """
    序列化参数
    """
    def __init__(self):
        self.out = []

    def ser_version(self, version):
        """
        :param version: 版本号
        """
        self.out.append(number_to_var_int(version))
        return self

    def ser_tx_type(self, type):
        """
        :param type: 交易类型
        """
        self.out.append(number_to_var_int(type))
        return self

    def ser_valid_height(self, height):
        """
        :param height: 区块高度
        """
        self.out.append(number_to_var_int(height))
        return self

    def ser_regid_or_public_key(self, regid, public_key):
        """
        :param regid: 用户的Id
        :param public_key: 账户的公钥
        """
        result = regid.split("-")
        if len(result) == 2:
            height = number_to_var_int(int(result[0]))
            index = number_to_var_int(int(result[1]))
            self.out.append(number_to_var_int(len(height) + len(index)))
            self.out.append(height)
            self.out.append(index)
        else:
            public_key_bytes = from_string_to_bytes(public_key)
            self.out.append(number_to_var_int(len(public_key_bytes)))
            self.out.append(public_key_bytes)
        return self

    def ser_regid(self, regid):
        """
        :param regid: register id
        """
        result = regid.split("-")
        height = number_to_var_int(int(result[0]))
        index = number_to_var_int(int(result[1]))
        self.out.append(number_to_var_int(len(height) + len(index)))
        self.out.append(height)
        self.out.append(index)
        return self

    def ser_desert_address(self, desert_address):
        """
            :param desert_address: 接受地址
            """
        address_bin = b58check_to_bin(desert_address)
        self.out.append(number_to_var_int(len(address_bin)))
        self.out.append(address_bin)
        return self

    def ser_fee(self, fee_amount, fee_coin_symbol):
        """
        :param fee_amount: 矿工费
        :param fee_coin_symbol: 矿工费币种
        """
        coin_symbol_byte = from_string_to_bytes(fee_coin_symbol)
        self.out.append(number_to_var_int(len(coin_symbol_byte)))
        self.out.append(coin_symbol_byte)
        self.out.append(number_to_var_int(fee_amount))
        return self

    def ser_fee_amount(self, amount):
        self.out.append(number_to_var_int(amount))
        return self

    def ser_coin_symbol(self, coin_symbol):
        coin_symbol_byte = from_string_to_bytes(coin_symbol)
        self.out.append(number_to_var_int(len(coin_symbol_byte)))
        self.out.append(coin_symbol_byte)
        return self

    def ser_coin_amount(self, amount):
        self.out.append(number_to_var_int(amount))
        return self

    def ser_order_id(self, order_id):
        self.out.append(number_str_to_bytes(order_id)[::-1])
        return self

    def ser_cdp_id(self, order_id):
        self.out.append(number_str_to_bytes(order_id)[::-1])
        return self

    def ser_cdp_stake_list(self, asset_list: [CdpStakeAsset]):
        self.out.append(number_to_var_int(len(asset_list)))
        for asset in asset_list:
            self.ser_coin_symbol(asset.symbol)
            self.ser_coin_amount(asset.amount)
        return self

    def ser_cdp_redeem_list(self, redeem_list: [CdpRedeemAsset]):
        self.out.append(number_to_var_int(len(redeem_list)))
        for asset in redeem_list:
            self.ser_coin_symbol(asset.symbol)
            self.ser_coin_amount(asset.amount)
        return self

    def ser_asset_type_and_value(self, type_, value):
        if type_ == 1:
            self.out.append(number_to_var_int(1))
            self.ser_regid(value)
        elif type_ == 2:
            self.out.append(number_to_var_int(2))
            self.ser_memo(value)
        elif type_ == 3:
            self.out.append(number_to_var_int(3))
            self.out.append(number_to_var_int(value))
        return self

    def ser_amount(self, amount, coin_symbol):
        """
        :param amount: 数量
        :param coin_symbol: 币种
        """
        coin_symbol_byte = from_string_to_bytes(coin_symbol)
        self.out.append(number_to_var_int(len(coin_symbol_byte)))
        self.out.append(coin_symbol_byte)
        self.out.append(number_to_var_int(amount))
        return self

    def ser_transfer(self, transfer_list: [Transfer]):
        """
        :param transfer_list: 转账列表
        """
        self.out.append(number_to_var_int(len(transfer_list)))
        for tf in transfer_list:
            address_bin = b58check_to_bin(tf.desert_address)
            self.out.append(number_to_var_int(len(address_bin)))
            self.out.append(address_bin)

            coin_symbol_byte = from_string_to_bytes(tf.pay_coin_symbol)
            self.out.append(number_to_var_int(len(coin_symbol_byte)))
            self.out.append(coin_symbol_byte)
            self.out.append(number_to_var_int(tf.pay_amount))
        return self

    def ser_memo(self, memo):
        """
        :param memo: 转账备注
        """
        memo_bytes = from_string_to_bytes(memo)
        self.out.append(number_to_var_int(len(memo_bytes)))
        self.out.append(memo_bytes)
        return self

    def ser_signature(self, signature):
        """
        :param signature: 签名
        """
        signature_bytes = number_str_to_bytes(signature)
        self.out.append(number_to_var_int(len(signature_bytes)))
        self.out.append(signature_bytes)
        return self

    def ser_contract_message(self, message):
        msg_bytes = number_str_to_bytes(message)
        self.out.append(number_to_var_int(len(msg_bytes)))
        self.out.append(msg_bytes)
        return self

    def to_bytes(self):
        return list_to_bytes(self.out)

    def to_hex_string(self):
        return bytes_to_hex_string(list_to_bytes(self.out))

    def to_message(self):
        return dbl_sha256_list(self.out)

    @classmethod
    def string_to_bytes(cls, string):
        return from_string_to_bytes(string)


def random_words():
    return entropy_to_words(os.urandom(16))


class Stamper(object):

    @classmethod
    def stamp(cls, message, private_key):
        """
        :param message: 需要签名的消息
        :param private_key: 私钥
        :return: 签名
        """
        return der_encode_sig(*ecdsa_raw_sign(message, private_key))

