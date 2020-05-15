import time
from .celeryconfig import app
from notify.notifyTasks import runCaseFailNotify, dayNotify, DEXNotify
from dex.tasks import DexTest
@app.task()
def yibu():
    print('start yibu')
    time.sleep(10)
    print('end yibu')

@app.task()
def dingshi():
    print('run dingshi')

@app.task()
def runcCaseFailNotifyTask():
    runCaseFailNotify()

@app.task()
def dayNotifyTask():
    dayNotify()

@app.task()
def DEXNotifyTask():
    DEXNotify()


@app.task()
def dextest():
    xt_test = DexTest('XT')
    xt_test.runTest()

    wicc_test = DexTest('WICC')
    wicc_test.runTest()

    wgrt_test = DexTest('WGRT')
    wgrt_test.runTest()

    xusd_test = DexTest('XUSD')
    xusd_test.runTest()

