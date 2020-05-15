import json
import random
from time import sleep
import requests
from dex.models import DEXTestResult
from dex.util.rpc_request import WiccRPC
from notify.dingding import dingTalk
from wicc.wallet import Wallet, DexLimitedPriceBuyTransaction, CoinType, DexLimitedPriceSellTransaction, \
    DexMarketPriceBuyTransaction, DexCancelOrderTransaction, DexMarketPriceSellTransaction

from tenacity import retry, stop_after_attempt, stop_after_delay, wait_fixed

from dex.util import DEXSign
import logging

logger = logging.getLogger(__name__)


# 保留6位小数
def get_float_six(f_str, n=6):
    f_str = str(f_str)
    a, b, c = f_str.partition('.')
    c = (c + "0" * n)[:n]  # 如论传入的函数有几位小数，在字符串后面都添加n为小数0
    return ".".join([a, c])


class Account:
    addr = None
    private_key = None
    reg_id = None
    open_txid_list = None

    def __init__(self, addr, private_key, reg_id):
        self.addr = addr
        self.private_key = private_key
        self.reg_id = reg_id


class DexTest:
    rpc = WiccRPC('http://10.0.0.31:6968', 'wayki', 'admin@123')

    depth = None

    buy_price_list = None
    sell_price_list = None
    buy_amount_list = None
    sell_amount_list = None
    sell_totalprice_list = None

    buy_account = Account('wZ6k2bzRK6jvueXPVDF6iMY4fgjqZyP8et', 'Y8NE6oK41i63RgiLcWcEBMaN64K4pBHGZyzSnj1phkgCktFUof8H',
                          '410420-2')
    sell_account = Account('wPp4M2KJVLE85ubvJ8iTAywu3QcJy7d4aR', 'Y6KfDubxttSA7xgn7EHMu2wj89f4HSre7dwCj8CUh5Wcgh29D5V9',
                           '8-2')

    # 传入交易资产
    def __init__(self, asset):
        self.asset = asset

    def runTest(self):
        logger.info('开始执行' + self.asset + '交易对测试 <————————————————————— start —————————————————————>')
        self.accountCancelOrder()
        try:
            self.limitBuy()
            self.limitBuy()
            self.limitSell()
            self.limitSell()
            self.marketBuy()
            self.marketSell()
            self.limitBuyDeal()
            self.limitSellDeal()
        except Exception as e:
            dingTalk(self.asset + '交易对执行用例失败:{}'.format(e) + "!!！！")

        finally:
            sleep(5)
            self.accountCancelOrder()
        logger.info('结束执行' + self.asset + '交易对测试 <————————————————————— end —————————————————————>')

    @retry(stop=(stop_after_attempt(10)), wait=wait_fixed(2), reraise=True)
    def getDepth(self):
        headers = {"Content-Type": "application/json;charset=UTF-8",
                   "Origin": "http://www.dex.devnet.waykitest.com",
                   "Referer": "http://www.dex.devnet.waykitest.com/"}
        data = {"limitNumber": 40,
                "tradePairCode": "{}_WUSD".format(self.asset)}
        try:
            rp = requests.post(url='http://www.dex.devnet.waykitest.com/api/dex/depth',
                               json=data, headers=headers)
            depth = eval(rp.text)
        except Exception as e:
            logger.info("get depth erro: {}".format([self.asset, depth, e]))
            raise "get depth erro: {}".format([self.asset, depth, e])

        self.buy_price_list = [float(buy['targetPrice']) for buy in depth['data']['buyList']]
        self.sell_price_list = [float(sell['targetPrice']) for sell in depth['data']['sellList']]
        self.buy_amount_list = [float(buy['pendingAmount']) for buy in depth['data']['buyList']]
        self.sell_amount_list = [float(sell['pendingAmount']) for sell in depth['data']['sellList']]
        self.sell_totalprice_list = [float(sell['pendingTotalPrice']) for sell in depth['data']['sellList']]

    @retry(stop=(stop_after_attempt(10)), wait=wait_fixed(2), reraise=True)
    def getHistory(self, addr):
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        data = {"address": addr, "currentpage": 1, "pagesize": 100,
                "tradePairCode": "{}_WUSD".format(self.asset)}
        try:
            rp = requests.post(url='http://www.dex.devnet.waykitest.com/api/dex/user/trade_history',
                               json=data, headers=headers)
        except Exception as e:
            logger.info('getHistory erro :{}'.format(e))
            raise 'getHistory erro :{}'.format(e)
        return json.loads(rp.text)

    @retry(stop=(stop_after_attempt(5)), wait=wait_fixed(1), reraise=True)
    def getOpenOrders(self, account: Account):
        headers = {"Content-Type": "application/json;charset=UTF-8"}
        data = {"address": account.addr,
                "tradePairCode": "{}_WUSD".format(self.asset)}

        try:
            rp = requests.post(url='http://www.dex.devnet.waykitest.com/api/dex/user/open_orders',
                               json=data, headers=headers)
            open_order = json.loads(rp.text)
            order_list = open_order['data']['list']
            if order_list:
                return [order['txHash'] for order in order_list]
        except Exception as e:
            logger.info('getOpenOrders erro ：{}'.format(e))
            raise 'getOpenOrders erro ：{}'.format(e)

    def accountCancelOrder(self):
        logger.info("start accountCancelOrder")
        buy_open_order_txid = self.getOpenOrders(self.buy_account)
        sell_open_order_txid = (self.getOpenOrders(self.sell_account))
        if buy_open_order_txid:
            for txid in buy_open_order_txid:
                sleep(3)
                DEXSign.cancelOrder(txid, self.buy_account)
        if sell_open_order_txid:
            for txid in sell_open_order_txid:
                sleep(3)
                DEXSign.cancelOrder(txid, self.sell_account)

    def limitBuy(self):

        self.getDepth()

        min_price = max(self.buy_price_list) * (10 ** 8)  # 最高买入价
        max_price = min(self.sell_price_list) * (10 ** 8)  # 最低卖出价
        avg_price = (min_price + max_price) / 2  # 平均价
        price = random.randrange(int(min_price) + 10, int(avg_price) - 10)  # 在最高买入价 - 平均价 之间取值，偏移1000，避免重合
        amount = (random.randrange(10, 30)) * (10 ** 8)

        result = DEXSign.limitBuy(self.buy_account, self.asset, amount, price)
        tx_id = result[0]['txid']

        price = price / (10 ** 8)
        amount = amount / (10 ** 8)
        totalPrice = price * amount
        logger.info('限价买单 {}'.format([price, amount, totalPrice]))

        status = self.assertOpenOrder(self.buy_account, tx_id)
        self.saveResult(1, status, self.asset, remark=tx_id)

    def limitBuyDeal(self):

        self.getDepth()

        price = int(self.sell_price_list[-2] * (10 ** 8)) + 10
        amount1 = self.sell_amount_list[-1] * (10 ** 8)
        amount2 = self.sell_amount_list[-2] * (10 ** 8)
        amount = int(amount1) + int(amount2 / 2)

        result = DEXSign.limitBuy(self.buy_account, self.asset, amount, price)
        txid = result[0]['txid']

        price = price / (10 ** 8)
        amount = amount / (10 ** 8)
        totalPrice = price * amount
        logger.info('限价买单-成交 {}'.format([price, amount, totalPrice]))

        total_price1 = self.sell_amount_list[-1] * self.sell_price_list[-1]
        total_price2 = self.sell_amount_list[-2] / 2 * self.sell_price_list[-2]
        predict_total_price = total_price1 + total_price2
        logger.info('预估成交金额 {}'.format(predict_total_price))

        self.assertHistory(self.buy_account, txid)

        history = self.getHistory(self.buy_account.addr)
        real_total_price = history['data']['list'][0]['total']
        logger.info('实际成交金额 {}'.format(real_total_price))

        status = get_float_six(predict_total_price) == get_float_six(real_total_price)
        remark = str(predict_total_price) + ' ' + str(real_total_price)
        self.saveResult(2, status, self.asset, remark)

    def marketBuy(self):

        self.getDepth()

        max_amount = self.sell_totalprice_list[-1] * (10 ** 8)
        amount = int(random.randrange(int(max_amount / 3), int(max_amount / 3 * 2)))

        result = DEXSign.marketBuy(self.buy_account, self.asset, amount)
        txid = result[0]['txid']

        logger.info('市价买单 {}'.format(amount / (10 ** 8)))

        predict_amount = amount / (self.sell_price_list[-1] * (10 ** 8))
        logger.info('预估买入数量 {}'.format(predict_amount))

        self.assertHistory(self.buy_account, txid)

        history = self.getHistory(self.buy_account.addr)
        real_amount = history['data']['list'][0]['amount']
        logger.info('实际买入数量 {}'.format(real_amount))

        status = get_float_six(predict_amount) == get_float_six(real_amount)
        remark = str(predict_amount) + ' ' + str(real_amount)
        self.saveResult(3, status, self.asset, remark)

    def limitSell(self):

        self.getDepth()

        min_price = max(self.buy_price_list) * (10 ** 8)  # 最高买入价
        max_price = min(self.sell_price_list) * (10 ** 8)  # 最低卖出价
        avg_price = (min_price + max_price) / 2  # 平均价
        price = random.randrange(int(avg_price) + 10, int(max_price) - 10)
        amount = (random.randrange(10, 30)) * (10 ** 8)

        result = DEXSign.limitSell(self.sell_account, self.asset, amount, price)
        txid = result[0]['txid']

        price = price / (10 ** 8)
        amount = amount / (10 ** 8)
        totalPrice = price * amount
        logger.info('限价卖单 {}'.format([price, amount, totalPrice]))

        status = self.assertOpenOrder(self.sell_account, txid)

        self.saveResult(4, status, self.asset, txid)

    def limitSellDeal(self):

        self.getDepth()

        price = int(self.buy_price_list[1] * (10 ** 8)) - 10
        amount1 = self.buy_amount_list[0] * (10 ** 8)
        amount2 = self.buy_amount_list[1] * (10 ** 8)
        amount = int(amount1) + int(amount2 / 2)

        result = DEXSign.limitSell(self.sell_account, self.asset, amount, price)
        txid = result[0]['txid']

        price = price / (10 ** 8)
        amount = amount / (10 ** 8)
        totalPrice = price * amount
        logger.info('限价卖单-成交 {}'.format([price, amount, totalPrice]))

        predict_total_price1 = self.buy_amount_list[0] * self.buy_price_list[0]
        predict_total_price2 = self.buy_amount_list[1] / 2 * self.buy_price_list[1]
        predict_total_price = predict_total_price1 + predict_total_price2
        logger.info('预估成交金额 {}'.format(predict_total_price))

        self.assertHistory(self.sell_account, txid)

        history = self.getHistory(self.sell_account.addr)
        real_total_price = history['data']['list'][0]['total']
        logger.info('实际成交金额 {}'.format(real_total_price))

        status = get_float_six(predict_total_price) == get_float_six(real_total_price)
        remark = str(predict_total_price) + ' ' + str(real_total_price)
        self.saveResult(5, status, self.asset, remark)

    def marketSell(self):

        self.getDepth()

        max_amount = self.buy_amount_list[0] * (10 ** 8)
        amount = random.randrange(int(max_amount / 3), int(max_amount / 3 * 2))

        result = DEXSign.marketSell(self.sell_account, self.asset, amount)
        txid = result[0]['txid']

        logger.info('市价卖单 {}'.format([amount / (10 ** 8)]))

        predict_total_price = amount / (10 ** 8) * self.buy_price_list[0]
        logger.info('预估卖出金额 {}'.format([predict_total_price]))

        self.assertHistory(self.sell_account, txid)

        history = self.getHistory(self.sell_account.addr)
        real_total_price = history['data']['list'][0]['total']
        logger.info('实际卖出金额 {}'.format([real_total_price]))

        status = get_float_six(predict_total_price) == get_float_six(real_total_price)
        remark = str(predict_total_price) + ' ' + str(real_total_price)
        self.saveResult(6, status, self.asset, remark)

    @retry(stop=(stop_after_attempt(10)), wait=wait_fixed(2), reraise=True)
    def saveResult(self, case_type, status, symbol, remark=''):
        try:
            test_result = DEXTestResult()
            test_result.case_type = case_type
            test_result.status = status
            test_result.symbol = symbol
            test_result.remark = remark
            test_result.save()
            logger.info('提交记录成功 {}'.format(case_type))
        except Exception as e:
            logger.info('提交测试结果出现异常，正在重试: {}'.format(e))
            raise '提交测试结果出现异常，正在重试: {}'.format(e)

    @retry(stop=(stop_after_attempt(10)), wait=wait_fixed(10), reraise=True)
    def assertOpenOrder(self, account: Account, tx_id):
        open_orders = self.getOpenOrders(account)
        if tx_id not in open_orders:
            logger.info("未找到目标txid：{}".format(tx_id))
            raise Exception("未找到目标txid：{}".format(tx_id))
        return True

    @retry(stop=(stop_after_attempt(10)), wait=wait_fixed(10), reraise=True)
    def assertHistory(self, account: Account, tx_id):
        history = self.getHistory(account.addr)
        tx_id_list = [order['txHash'] for order in history['data']['list']]
        if tx_id not in tx_id_list:
            logger.info("未找到目标txid：{}".format(tx_id))
            raise Exception("未找到目标txid：{}".format(tx_id))


if __name__ == '__main__':
    dextest = DexTest('XT')
    # dextest.runTest()
    # dextest.getHistory()
    # dextest.getDepth()
    # dextest.getOpenOrders()
