import json
import random
from decimal import Decimal
from time import sleep

import requests
from dex.util import dex
from dex.util.rpc_request import WiccRPC
from wicc.wallet import Wallet, DexLimitedPriceBuyTransaction, CoinType, DexLimitedPriceSellTransaction, \
    DexMarketPriceBuyTransaction, DexCancelOrderTransaction, DexMarketPriceSellTransaction


class Account:
    addr = None
    private_key = None
    reg_id = None
    tx_id_list = []

    def __init__(self, addr, private_key, reg_id):
        self.addr = addr
        self.private_key = private_key
        self.reg_id = reg_id


class DexTest:
    rpc = WiccRPC('http://10.0.0.31:6968', 'wayki', 'admin@123')

    depth = None
    history = None
    buy_price_list = None
    sell_price_list = None
    buy_amount_list = None
    sell_amount_list = None
    sell_totalprice_list = None

    assert_list = []

    buy_account = Account('wZ6k2bzRK6jvueXPVDF6iMY4fgjqZyP8et', 'Y8NE6oK41i63RgiLcWcEBMaN64K4pBHGZyzSnj1phkgCktFUof8H',
                          '410420-2')
    sell_account = Account('wPp4M2KJVLE85ubvJ8iTAywu3QcJy7d4aR', 'Y6KfDubxttSA7xgn7EHMu2wj89f4HSre7dwCj8CUh5Wcgh29D5V9',
                           '8-2')

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
            except Exception as e:
                print('getDepth erro', e)
                sleep(1)

        self.buy_price_list = [float(buy['targetPrice']) for buy in self.depth['data']['buyList']]
        self.sell_price_list = [float(sell['targetPrice']) for sell in self.depth['data']['sellList']]
        self.buy_amount_list = [float(buy['pendingAmount']) for buy in self.depth['data']['buyList']]
        self.sell_amount_list = [float(sell['pendingAmount']) for sell in self.depth['data']['sellList']]
        self.sell_totalprice_list = [float(sell['pendingTotalPrice']) for sell in self.depth['data']['sellList']]

    def getHistory(self, addr):
        sleep(30)
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        data = {"address": addr, "currentpage": 1, "pagesize": 100,
                "tradePairCode": "XT_WUSD"}
        while True:
            try:
                rp = requests.post(url='http://www.dex.devnet.waykitest.com/api/dex/user/trade_history',
                                   json=data, headers=headers)

                self.history = json.loads(rp.text)
                break
            except Exception as e:
                print('getHistory erro', e)
                sleep(1)

    def limitBuy(self):

        self.getDepth()

        min_price = max(self.buy_price_list) * (10 ** 8)  # 最高买入价
        max_price = min(self.sell_price_list) * (10 ** 8)  # 最低卖出价
        avg_price = (min_price + max_price) / 2  # 平均价
        price = random.randrange(int(min_price) + 1000, int(avg_price) - 1000)  # 在最高买入价 - 平均价 之间取值，偏移1000，避免重合
        amount = (random.randrange(10, 100)) * (10 ** 8)

        # 提交RPC
        # result = dex.buylimit('wNDue1jHcgRSioSDL4o1AzXz3D72gCMkP6', 'WUSD', 'XT:1000000000:sawi', 100000000, 0)
        # print(result)

        # 离线签名
        wallet = Wallet(self.buy_account.private_key)

        tr = DexLimitedPriceBuyTransaction()
        tr.fee_amount = 10000000
        tr.fee_coin_symbol = CoinType.WICC.value
        tr.valid_height = self.rpc.call('getinfo', [])[0]['synblock_height']
        tr.register_id = self.buy_account.reg_id
        tr.coin_symbol = CoinType.WUSD.value
        tr.asset_symbol = CoinType.XT.value
        tr.asset_amount = amount
        tr.price = price
        rawtx = wallet.dex_limited_price_buy_tx(tr)
        result = self.rpc.call('submittxraw', [rawtx])
        self.buy_account.tx_id_list.append(result[0]['txid'])

        price = price / (10 ** 8)
        amount = amount / (10 ** 8)
        totalPrice = price * amount
        print('限价买单', price, amount, totalPrice)

    def limitBuyDeal(self):

        self.getDepth()

        price = int(self.sell_price_list[-2] * (10 ** 8))
        amount1 = self.sell_amount_list[-1] * (10 ** 8)
        amount2 = self.sell_amount_list[-2] * (10 ** 8)
        amount = int(amount1) + int(amount2 / 2)

        # 提交RPC
        # result = dex.buylimit('wNDue1jHcgRSioSDL4o1AzXz3D72gCMkP6', 'WUSD', 'XT:1000000000:sawi', 100000000, 0)
        # print(result)

        # 离线签名
        wallet = Wallet(self.buy_account.private_key)

        tr = DexLimitedPriceBuyTransaction()
        tr.fee_amount = 10000000
        tr.fee_coin_symbol = CoinType.WICC.value
        tr.valid_height = self.rpc.call('getinfo', [])[0]['synblock_height']
        tr.register_id = self.buy_account.reg_id
        tr.coin_symbol = CoinType.WUSD.value
        tr.asset_symbol = CoinType.XT.value
        tr.asset_amount = amount
        tr.price = price
        rawtx = wallet.dex_limited_price_buy_tx(tr)
        result = self.rpc.call('submittxraw', [rawtx])
        self.buy_account.tx_id_list.append(result[0]['txid'])

        price = price / (10 ** 8)
        amount = amount / (10 ** 8)
        totalPrice = price * amount
        print('限价买单-成交', price, amount, totalPrice)

        totalPrice1 = self.sell_amount_list[-1] * self.sell_price_list[-1]
        totalPrice2 = self.sell_amount_list[-2] / 2 * self.sell_price_list[-2]
        totalPrice = totalPrice1 + totalPrice2
        print('预估成交金额', totalPrice)


        self.getHistory(self.buy_account.addr)
        total = self.history['data']['list'][0]['total']
        print('实际成交金额', total)

        self.assert_list.append(Decimal(str(totalPrice)).quantize('0.000000') == Decimal(str(total)).quantize('0.000000'))

    def marketBuy(self):

        self.getDepth()

        max_amount = self.sell_totalprice_list[-1] * (10 ** 8)
        amount = int(random.randrange(int(max_amount / 3), int(max_amount / 3 * 2)))
        wallet = Wallet(self.buy_account.private_key)
        tr = DexMarketPriceBuyTransaction()
        tr.fee_amount = 10000000
        tr.fee_coin_symbol = CoinType.WICC.value
        tr.valid_height = self.rpc.call('getinfo', [])[0]['synblock_height']
        tr.register_id = self.buy_account.reg_id
        tr.coin_symbol = CoinType.WUSD.value
        tr.coin_amount = amount
        tr.asset_symbol = CoinType.XT.value
        rawtx = wallet.dex_market_price_buy_tx(tr)
        result = self.rpc.call('submittxraw', [rawtx])
        self.buy_account.tx_id_list.append(result[0]['txid'])

        print('市价买单', amount / (10 ** 8))

        predict_amount = amount / (self.sell_price_list[-1] * (10 ** 8))
        print('预估买入数量', predict_amount)


        self.getHistory(self.buy_account.addr)
        real_amount = self.history['data']['list'][0]['amount']
        print('实际买入数量', real_amount)

        self.assert_list.append(Decimal(str(predict_amount)).quantize('0.000000') == Decimal(str(real_amount)).quantize('0.000000'))

        print(self.assert_list)

    def limitSell(self):

        self.getDepth()

        min_price = max(self.buy_price_list) * (10 ** 8)  # 最高买入价
        max_price = min(self.sell_price_list) * (10 ** 8)  # 最低卖出价
        avg_price = (min_price + max_price) / 2  # 平均价
        price = random.randrange(int(avg_price) + 1000, int(max_price) - 1000)
        amount = (random.randrange(10, 100)) * (10 ** 8)

        wallet = Wallet(self.sell_account.private_key)
        tr = DexLimitedPriceSellTransaction()
        tr.fee_amount = 10000000
        tr.fee_coin_symbol = CoinType.WICC.value
        tr.valid_height = self.rpc.call('getinfo', [])[0]['synblock_height']
        tr.register_id = self.sell_account.reg_id
        tr.coin_symbol = CoinType.WUSD.value
        tr.asset_symbol = CoinType.XT.value
        tr.asset_amount = amount
        tr.price = price
        rawtx = wallet.dex_limited_price_sell_tx(tr)
        result = self.rpc.call('submittxraw', [rawtx])
        self.sell_account.tx_id_list.append(result[0]['txid'])

        price = price / (10 ** 8)
        amount = amount / (10 ** 8)
        totalPrice = price * amount
        print('限价卖单', price, amount, totalPrice)

    def limitSellDeal(self):

        self.getDepth()

        price = int(self.buy_price_list[1] * (10 ** 8))
        amount1 = self.buy_amount_list[0] * (10 ** 8)
        amount2 = self.buy_amount_list[1] * (10 ** 8)
        amount = int(amount1) + int(amount2 / 2)

        wallet = Wallet(self.sell_account.private_key)
        tr = DexLimitedPriceSellTransaction()
        tr.fee_amount = 10000000
        tr.fee_coin_symbol = CoinType.WICC.value
        tr.valid_height = self.rpc.call('getinfo', [])[0]['synblock_height']
        tr.register_id = self.sell_account.reg_id
        tr.coin_symbol = CoinType.WUSD.value
        tr.asset_symbol = CoinType.XT.value
        tr.asset_amount = amount
        tr.price = price
        rawtx = wallet.dex_limited_price_sell_tx(tr)
        result = self.rpc.call('submittxraw', [rawtx])
        self.sell_account.tx_id_list.append(result[0]['txid'])

        price = price / (10 ** 8)
        amount = amount / (10 ** 8)
        totalPrice = price * amount
        print('限价卖单-成交', price, amount, totalPrice)

        totalPrice1 = self.buy_amount_list[0] * self.buy_price_list[0]
        totalPrice2 = self.buy_amount_list[1] / 2 * self.buy_price_list[1]
        print('预估成交金额', totalPrice1 + totalPrice2)


        self.getHistory(self.sell_account.addr)
        print('实际成交金额', self.history['data']['list'][0]['total'])

    def marketSell(self):

        self.getDepth()

        max_amount = self.buy_amount_list[0] * (10 ** 8)
        amount = random.randrange(int(max_amount / 3), int(max_amount / 3 * 2))
        wallet = Wallet(self.sell_account.private_key)
        tr = DexMarketPriceSellTransaction()
        tr.fee_amount = 10000000
        tr.fee_coin_symbol = CoinType.WICC.value
        tr.valid_height = self.rpc.call('getinfo', [])[0]['synblock_height']
        tr.register_id = self.sell_account.reg_id
        tr.coin_symbol = CoinType.WUSD.value
        tr.asset_symbol = CoinType.XT.value
        tr.asset_amount = amount
        rawtx = wallet.dex_market_price_sell_tx(tr)
        result = self.rpc.call('submittxraw', [rawtx])
        self.sell_account.tx_id_list.append(result[0]['txid'])

        print('市价卖单', amount / (10 ** 8))

        totalPrice = amount / (10 ** 8) * self.buy_price_list[0]
        print('预估卖出金额', totalPrice)


        self.getHistory(self.sell_account.addr)
        print('实际卖出金额', self.history['data']['list'][0]['total'])

    def cancelOrder(self, txid, account: Account):
        wallet = Wallet(account.private_key)
        tr = DexCancelOrderTransaction()
        tr.fee_amount = 1000000
        tr.fee_coin_symbol = CoinType.WICC.value
        tr.valid_height = self.rpc.call('getinfo', [])[0]['synblock_height']
        tr.register_id = account.reg_id
        tr.order_id = txid
        rawtx = wallet.dex_cancel_order_tx(tr)
        result = self.rpc.call('submittxraw', [rawtx])
        print(result)

    def runTest(self):
        try:
            self.limitBuy()
            sleep(5)
            self.limitBuy()
            sleep(5)
            self.limitSell()
            sleep(5)
            self.limitSell()
            sleep(15)
            self.marketBuy()
            sleep(15)
            self.marketSell()
            sleep(15)
            self.limitBuyDeal()
            sleep(15)
            self.limitSellDeal()
        except Exception as e:
            raise e
        finally:
            sleep(15)
            for tx_id in self.buy_account.tx_id_list:
                sleep(3)
                self.cancelOrder(tx_id, self.buy_account)
            for tx_id in self.sell_account.tx_id_list:
                sleep(3)
                self.cancelOrder(tx_id, self.sell_account)


if __name__ == '__main__':
    dextest = DexTest()
    dextest.runTest()
    # dextest.getHistory()
    # dextest.getDepth()
