#!/usr/bin/python
# -*- coding: utf-8 -*-
from enum import Enum


class TxType(Enum):
    """
    交易类型
    transaction type
    """
    COMMON = 3
    CONTRACT = 4
    CONTRACT_DEPLOY = 5
    DELEGATE = 6

    ASSET_ISSUE = 9
    ASSET_UPDATE = 10

    U_COIN_TRANSFER = 11
    U_CONTRACT_DEPLOY = 14
    U_CONTRACT_INVOKE = 15

    CDP_STAKE = 21
    CDP_REDEEM = 22
    CDP_LIQUIDATE = 23

    DEX_LIMITED_PRICE_BUY_ORDER = 84
    DEX_LIMITED_PRICE_SELL_ORDER = 85
    DEX_MARKET_PRICE_BUY_ORDER = 86
    DEX_MARKET_PRICE_SELL_ORDER = 87
    DEX_CANCEL_ORDER = 88


class VoteType(Enum):
    """
    投票类型
    """
    ADD = 1
    MINUS = 1


class AssetUpdateType(Enum):
    """

    """
    NONE = 0
    OWNER_UID = 1
    NAME = 2
    MINT_AMOUNT = 3


class CoinType(Enum):
    WICC ="WICC"
    WUSD = "WUSD"
    WGRT = "WICC"
    WCNY = "WCNY"
    WBTC = "WBTC"
    WETH = "WETH"
    WEOS = "WEOS"
    USD = "USD"
    CNY = "CNY"
    EUR = "EUR"
    BTC = "BTC"
    USDT = "USDT"
    GOLD = "GOLD"
    KWH = "KWH"
    XT = "XT"
    XUSD = "XUSD"


class Transfer(object):

    def __init__(self, amount, symbol, desert_address):
        """
        :param amount: 支付的数量
        :param symbol: 支付的币种
        :param desert_address: 支付到的地址
        """
        self.pay_amount = amount
        self.pay_coin_symbol = symbol
        self.desert_address = desert_address


class Vote(object):

    def __init__(self, vote_type, pub_key, amount):
        """
        :param type: 投票类型
        :param pub_key: 接受投票账号的公钥
        :param amount: 投票的数量
        """
        self.type = vote_type
        self.pub_key = pub_key
        self.amount = amount


class BaseTransaction(object):
    """
    交易基类
    """
    def __init__(self):
        self.valid_height = 0
        self.register_id = ""
        self.fee_amount = 0
        self.fee_coin_symbol = ""
        self.memo = ""


class TransferTransaction(BaseTransaction):
    """
    转账交易
    """
    def __init__(self):
        super().__init__()
        #self.transfer_list: {Transfer} = []


class VoteTransaction(BaseTransaction):
    """
    投票交易
    """
    def __init__(self):
        super().__init__()
        #self.vote_list: [Vote] = []


class ContractDeployTransaction(BaseTransaction):
    """
    合约部署交易
    """
    def __init__(self):
        super().__init__()
        self.contract_byte = ""
        self.description = ""


class ContractCallTransaction(BaseTransaction):
    """
     合约调用交易
     """
    def __init__(self):
        super().__init__()
        self.app_id = ""
        self.contract_call_msg = ""
        self.pay_amount = 0
        self.pay_coin_symbol = ""


class ContractDeployTransaction(BaseTransaction):
    """
    合约部署
    """
    def __init__(self):
        super().__init__()
        self.file_path = ""


class DexLimitedPriceBuyTransaction(BaseTransaction):
    """
    限价买单交易
    """
    def __init__(self):
        super().__init__()
        self.fee_amount = 10000000
        self.coin_symbol = ""
        self.asset_symbol= ""
        self.asset_amount = ""
        self.price = 100000


class DexLimitedPriceSellTransaction(BaseTransaction):
    """
    限价卖单交易
    """
    def __init__(self):
        super().__init__()
        self.fee_amount = 10000000
        self.coin_symbol = ""
        self.asset_symbol= ""
        self.asset_amount = ""
        self.price = 100000


class DexMarketPriceBuyTransaction(BaseTransaction):
    """
    市价买单交易
    """
    def __init__(self):
        super().__init__()
        self.fee_amount = 10000000
        self.coin_symbol = ""
        self.coin_amount = 0
        self.asset_symbol= ""



class DexMarketPriceSellTransaction(BaseTransaction):
    """
    市价卖单交易
    """
    def __init__(self):
        super().__init__()
        self.fee_amount = 10000000
        self.coin_symbol = ""
        self.asset_symbol= ""
        self.asset_amount = ""


class DexCancelOrderTransaction(BaseTransaction):
    """
    取消挂单交易
    """
    def __init__(self):
        super().__init__()
        self.order_id = ""


class CdpStakeAsset(object):
    """
    Cdp抵押的资产
    """
    def __init__(self, symbol, amount):
        self.symbol = symbol
        self.amount = amount


class CdpStakeTransaction(BaseTransaction):
    """
    创建,追加cdp交易
    """
    def __init__(self):
        super().__init__()
        self.cdp_id = "0000000000000000000000000000000000000000000000000000000000000000"
        self.stake_list = []
        self.get_coin_symbol = ""
        self.get_amount = 0


class CdpRedeemAsset(object):
    """
    Cdp赎回的资产
    """
    def __init__(self, symbol, amount):
        self.symbol = symbol
        self.amount = amount


class CdpRedeemTransaction(BaseTransaction):
    """
    赎回cdp交易
    """
    def __init__(self):
        super().__init__()
        self.cdp_id = "0000000000000000000000000000000000000000000000000000000000000000"
        self.free_coin_symbol = ""
        self.repay_amount = 0
        self.free_amount = 0
        self.redeem_list = []


class CdpLiquidateTransaction(BaseTransaction):
    """
    清算cdp交易
    """
    def __init__(self):
        super().__init__()
        self.cdp_id = "0000000000000000000000000000000000000000000000000000000000000000"
        self.free_coin_symbol = ""
        self.liquidate_coin_symbol = 0
        self.liquidate_amount = 0


class AssetPublishTransaction(BaseTransaction):
    """
    资产发布交易
    """
    def __init__(self):
        super().__init__()
        self.asset_symbol = ""
        self.asset_update_type = 0
        self.asset_update_value = ""





