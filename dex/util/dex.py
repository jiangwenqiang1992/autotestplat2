import random
from decimal import Decimal

from dex.util.rpc_request import WiccRPC
from dex.util.json_format_print import printJson

rpc = WiccRPC('http://10.0.0.31:6968', 'wayki', 'admin@123')

# 订单查询
def getdexorder(orderId):
    result = rpc.call('getdexorder', [orderId])
    # printJson(result)
    return result


# 根据高度区间，查询订单
def getdexorders(begin_height, end_height, max_count):
    result = rpc.call('getdexorders', [begin_height, end_height, max_count])
    # printJson(result)
    return result


# 查询区块的系统订单
def getdexsysorders(height):
    result = rpc.call('getdexsysorders', [height])
    # printJson(result)
    return result


# 提交限价买入单
def buylimit(addr, coin, asset_amount_unit, price, dex_id):
    #asset_amount = Decimal(str(asset_amount)) * Decimal(str(100000000))
    #price = Decimal(str(price)) * Decimal(str(100000000))
    #result = rpc.call('submitdexbuylimitordertx', [addr, coin, asset, float(asset_amount), float(price)])
    result = rpc.call('submitdexbuylimitordertx', [addr, coin, asset_amount_unit, price, dex_id])
    # printJson(result)
    return result


# 提交限价卖出单
def selllimit(addr, coin, asset, asset_amount, price):
    asset_amount = Decimal(str(asset_amount)) * Decimal(str(100000000))
    price = Decimal(str(price)) * Decimal(str(100000000))
    result = rpc.call('submitdexselllimitordertx', [addr, coin, asset, float(asset_amount), float(price)])
    printJson(result)
    return result


# 提交市价买入单
def buymarket(addr, coin, coin_amount, asset):
    coin_amount = coin_amount * 100000000
    fee = 100000 + random.randint(1, 100)
    params = [addr, coin, coin_amount, asset, "WICC:{}:sawi".format(fee)]
    result = rpc.call('submitdexbuymarketordertx', params)
    printJson(result)


# 提交市价卖出单
def sellmarket(addr, coin, asset, asset_amount):
    asset_amount = asset_amount * 100000000
    fee = 100000 + random.randint(1, 100)
    params = [addr, coin, asset, asset_amount, "WICC:{}:sawi".format(fee)]
    result = rpc.call('submitdexsellmarketordertx', params)
    printJson(result)


# 取消订单
def cancel(addr, orderId):
    result = rpc.call('submitdexcancelordertx', [addr, orderId])
    # printJson(result)
    return result
