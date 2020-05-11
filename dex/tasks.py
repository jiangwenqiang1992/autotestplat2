import json
import random
from time import sleep

import requests
from dex.util import dex
from dex.util.rpc_request import WiccRPC
from wicc.wallet import Wallet, DexLimitedPriceBuyTransaction, CoinType, DexLimitedPriceSellTransaction, \
    DexMarketPriceBuyTransaction, DexCancelOrderTransaction, DexMarketPriceSellTransaction


class DexTest:
    rpc = WiccRPC('http://10.0.0.31:6968', 'wayki', 'admin@123')

    depth = None
    buy_price_list = None
    sell_price_list = None
    buy_amount_list = None
    sell_totalprice_list = None

    txid_list = []

    def getDepth(self):
        headers = {"Content-Type": "application/json;charset=UTF-8",
                   "Origin": "http://www.dex.devnet.waykitest.com",
                   "Referer": "http://www.dex.devnet.waykitest.com/"}
        data = {"limitNumber": 40,
                "tradePairCode": "XT_WUSD"}
        while True:
            try:
                rp = requests.post(url='http://www.dex.devnet.waykitest.com/api/dex/depth',
                                   json=data, headers=headers)
                self.depth = eval(rp.text)
                break
            except:
                sleep(1)

        self.buy_price_list = [float(buy['targetPrice']) for buy in self.depth['data']['buyList']]
        self.sell_price_list = [float(sell['targetPrice']) for sell in self.depth['data']['sellList']]
        self.buy_amount_list = [float(buy['amount']) for buy in self.depth['data']['buyList']]
        self.sell_totalprice_list = [float(sell['pendingTotalPrice']) for sell in self.depth['data']['sellList']]

    def limitBuy(self):

        self.getDepth()

        min_price = self.buy_price_list[0] * (10 ** 8)
        max_price = self.sell_price_list[-1] * (10 ** 8)
        avg_price = (min_price + max_price) / 2 - 1000
        price = random.randrange(min_price, int(avg_price))
        amount = (random.randrange(10, 100)) * (10 ** 8)

        # 提交RPC
        # result = dex.buylimit('wNDue1jHcgRSioSDL4o1AzXz3D72gCMkP6', 'WUSD', 'XT:1000000000:sawi', 100000000, 0)
        # print(result)

        # 离线签名
        wallet = Wallet("Y5F2GraTdQqMbYrV6MG78Kbg4QE8p4B2DyxMdLMH7HmDNtiNmcbM")

        tr = DexLimitedPriceBuyTransaction()
        tr.fee_amount = 10000000
        tr.fee_coin_symbol = CoinType.WICC.value
        tr.valid_height = self.rpc.call('getinfo', [])[0]['synblock_height']
        tr.register_id = "0-2"
        tr.coin_symbol = CoinType.WUSD.value
        tr.asset_symbol = CoinType.XT.value
        tr.asset_amount = amount
        tr.price = price
        rawtx = wallet.dex_limited_price_buy_tx(tr)
        result = self.rpc.call('submittxraw', [rawtx])
        self.txid_list.append(result[0]['txid'])

    def limitSell(self):

        self.getDepth()

        min_price = self.buy_price_list[0] * (10 ** 8) + 1000
        max_price = self.sell_price_list[-1] * (10 ** 8) - 1000
        avg_price = (min_price + max_price) / 2 + 1000
        price = random.randrange(int(avg_price), max_price)
        amount = (random.randrange(10, 100)) * (10 ** 8)

        wallet = Wallet("Y5F2GraTdQqMbYrV6MG78Kbg4QE8p4B2DyxMdLMH7HmDNtiNmcbM")
        tr = DexLimitedPriceSellTransaction()
        tr.fee_amount = 10000000
        tr.fee_coin_symbol = CoinType.WICC.value
        tr.valid_height = self.rpc.call('getinfo', [])[0]['synblock_height']
        tr.register_id = "0-2"
        tr.coin_symbol = CoinType.WUSD.value
        tr.asset_symbol = CoinType.XT.value
        tr.asset_amount = amount
        tr.price = price
        rawtx = wallet.dex_limited_price_sell_tx(tr)
        result = self.rpc.call('submittxraw', [rawtx])
        self.txid_list.append(result[0]['txid'])

    def marketBuy(self):

        self.getDepth()

        max_amount = self.sell_totalprice_list[-1]*(10**8)
        amount = int(random.randrange(int(max_amount / 3), int(max_amount / 3 * 2)))
        wallet = Wallet("Y5F2GraTdQqMbYrV6MG78Kbg4QE8p4B2DyxMdLMH7HmDNtiNmcbM")
        tr = DexMarketPriceBuyTransaction()
        tr.fee_amount = 10000000
        tr.fee_coin_symbol = CoinType.WICC.value
        tr.valid_height = self.rpc.call('getinfo', [])[0]['synblock_height']
        tr.register_id = "0-2"
        tr.coin_symbol = CoinType.WUSD.value
        tr.coin_amount = amount
        tr.asset_symbol = CoinType.XT.value
        rawtx = wallet.dex_market_price_buy_tx(tr)
        result = self.rpc.call('submittxraw', [rawtx])
        self.txid_list.append(result[0]['txid'])

    def marketSell(self):

        self.getDepth()

        max_amount = self.buy_amount_list[0]*(10**8)
        amount = random.randrange(int(max_amount / 3), int(max_amount / 3 * 2))
        wallet = Wallet("Y5F2GraTdQqMbYrV6MG78Kbg4QE8p4B2DyxMdLMH7HmDNtiNmcbM")
        tr = DexMarketPriceSellTransaction()
        tr.fee_amount = 10000000
        tr.fee_coin_symbol = CoinType.WICC.value
        tr.valid_height = self.rpc.call('getinfo', [])[0]['synblock_height']
        tr.register_id = "0-2"
        tr.coin_symbol = CoinType.WUSD.value
        tr.asset_symbol = CoinType.XT.value
        tr.asset_amount = amount
        rawtx = wallet.dex_market_price_sell_tx(tr)
        result = self.rpc.call('submittxraw', [rawtx])
        self.txid_list.append(result[0]['txid'])

    def cancelOrder(self,txid):
        wallet = Wallet("Y5F2GraTdQqMbYrV6MG78Kbg4QE8p4B2DyxMdLMH7HmDNtiNmcbM")
        tr = DexCancelOrderTransaction()
        tr.fee_amount = 1000000
        tr.fee_coin_symbol = CoinType.WICC.value
        tr.valid_height = self.rpc.call('getinfo', [])[0]['synblock_height']
        tr.register_id = "0-2"
        tr.order_id = txid
        rawtx = wallet.dex_cancel_order_tx(tr)
        result = self.rpc.call('submittxraw', [rawtx])
        print(result)

    def runTest(self):
        self.limitBuy()
        sleep(3)
        self.limitBuy()
        sleep(3)
        self.limitSell()
        sleep(3)
        self.limitSell()
        sleep(3)
        self.marketBuy()
        sleep(3)
        self.marketSell()

        sleep(10)
        for tx_id in self.txid_list:
            sleep(3)
            self.cancelOrder(tx_id)


if __name__ == '__main__':
    dextest = DexTest()
    dextest.runTest()
