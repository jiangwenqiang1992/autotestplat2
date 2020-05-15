from dex.util.rpc_request import WiccRPC
from wicc.transactions import DexLimitedPriceBuyTransaction, CoinType, DexMarketPriceBuyTransaction, \
    DexLimitedPriceSellTransaction, DexMarketPriceSellTransaction, DexCancelOrderTransaction
from wicc.wallet import Wallet

rpc = WiccRPC('http://10.0.0.31:6968', 'wayki', 'admin@123')


def getHeight():
    return rpc.call('getinfo', [])[0]['synblock_height']


def limitBuy(account, asset, amount, price):
    wallet = Wallet(account.private_key)

    tr = DexLimitedPriceBuyTransaction()
    tr.fee_amount = 10000000
    tr.fee_coin_symbol = CoinType.WICC.value
    tr.valid_height = getHeight()
    tr.register_id = account.reg_id
    tr.coin_symbol = CoinType.WUSD.value
    tr.asset_symbol = asset
    tr.asset_amount = amount
    tr.price = price
    rawtx = wallet.dex_limited_price_buy_tx(tr)
    return rpc.call('submittxraw', [rawtx])


def marketBuy(account, asset, amount):
    wallet = Wallet(account.private_key)
    tr = DexMarketPriceBuyTransaction()
    tr.fee_amount = 10000000
    tr.fee_coin_symbol = CoinType.WICC.value
    tr.valid_height = getHeight()
    tr.register_id = account.reg_id
    tr.coin_symbol = CoinType.WUSD.value
    tr.coin_amount = amount
    tr.asset_symbol = asset
    rawtx = wallet.dex_market_price_buy_tx(tr)
    return rpc.call('submittxraw', [rawtx])

def limitSell(account, asset, amount, price):
    wallet = Wallet(account.private_key)
    tr = DexLimitedPriceSellTransaction()
    tr.fee_amount = 10000000
    tr.fee_coin_symbol = CoinType.WICC.value
    tr.valid_height = getHeight()
    tr.register_id = account.reg_id
    tr.coin_symbol = CoinType.WUSD.value
    tr.asset_symbol = asset
    tr.asset_amount = amount
    tr.price = price
    rawtx = wallet.dex_limited_price_sell_tx(tr)
    return rpc.call('submittxraw', [rawtx])

def marketSell(account, asset, amount):
    wallet = Wallet(account.private_key)
    tr = DexMarketPriceSellTransaction()
    tr.fee_amount = 10000000
    tr.fee_coin_symbol = CoinType.WICC.value
    tr.valid_height = getHeight()
    tr.register_id = account.reg_id
    tr.coin_symbol = CoinType.WUSD.value
    tr.asset_symbol = asset
    tr.asset_amount = amount
    rawtx = wallet.dex_market_price_sell_tx(tr)
    return rpc.call('submittxraw', [rawtx])

def cancelOrder(txid, account):
    wallet = Wallet(account.private_key)
    tr = DexCancelOrderTransaction()
    tr.fee_amount = 1000000
    tr.fee_coin_symbol = CoinType.WICC.value
    tr.valid_height = getHeight()
    tr.register_id = account.reg_id
    tr.order_id = txid
    rawtx = wallet.dex_cancel_order_tx(tr)
    result = rpc.call('submittxraw', [rawtx])
    return result