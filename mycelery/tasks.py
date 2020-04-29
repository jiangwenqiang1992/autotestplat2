import time
from .celeryconfig import app
from notify.notifyTasks import runCaseFailNotify,dayNotify

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
