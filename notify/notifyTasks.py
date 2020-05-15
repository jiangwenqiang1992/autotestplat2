import datetime
from time import sleep

import pymysql as pymysql
from django.http import HttpResponse

from result.models import ResultCount
from io import StringIO
from .dingding import dingTalk

def runCaseFailNotify():
    result_fail_list = ResultCount.objects.filter(notify_status=0).all()
    messge = StringIO()
    fail_count = 0
    for result in result_fail_list:
        fail_count += result.fail_count
        if result.fail_count>0:
            messge.write("任务名称：{}".format(result.jobname)+'\n')
            messge.write("用例数量：{}".format(result.run_count) + '\n')
            messge.write("通过数量：{}".format(result.pass_count) + '\n')
            messge.write("失败数量：{}".format(result.fail_count) + '\n')
            messge.write("执行时间：{}".format(str(result.create_time).split('.')[0]) + '\n')
            messge.write('\n')
        result.notify_status = 1
        result.save()
    if len(result_fail_list) > 0 and fail_count > 0:
        messge.write('！！\n')
        dingTalk(messge.getvalue())
    return messge.getvalue()



from django.db.models import Count, Max, Sum
def dayNotify():
    time = datetime.datetime.now() + datetime.timedelta(days=int(-1))
    result_fail_list = ResultCount.objects.filter(create_time__gt=time)\
        .values("jobname").annotate(count=Count('id'), max=Max('create_time'), runsum=Sum('run_count'),  runfail=Sum('fail_count'))\
        .values('jobname','count','runsum','runfail','max')
    messge = StringIO()

    for reuslt in result_fail_list:
        messge.write("任务名称：{}".format(reuslt['jobname'])+'\n')
        messge.write("运行次数：{}".format(reuslt['count']) + '\n')
        messge.write("用例数量：{}".format(reuslt['runsum']) + '\n')
        messge.write("错误数量：{}".format(reuslt['runfail']) + '\n')
        messge.write("最近运行：{}".format(str(reuslt['max']).split('.')[0]) + '\n')
        messge.write('\n')

    if len(result_fail_list):
        messge.write('！！\n')
        dingTalk(messge.getvalue())
    return messge.getvalue()


def DEXNotify():
    sql = "select case_type, MAX(CASE `status` WHEN 1 THEN num ELSE 0 END ) as '1', MAX(CASE `status` WHEN 0 THEN num ELSE 0 END ) as '0' from (SELECT COUNT(*) as num,`status`,case_type  FROM dex_dextestresult WHERE create_time > DATE_ADD( DATE_ADD( NOW(),interval -8 hour),interval -1 day) GROUP BY case_type,`status`) temp group by case_type ORDER BY case_type"

    while True:
        try:
            coon = pymysql.connect(user='root', passwd='txy431026.', db='auto2', port=3306, host='119.29.129.239')
            cursor = coon.cursor()
            aa = cursor.execute(sql)
            info = cursor.fetchmany(aa)
            break
        except:
            sleep(1)
    try:
        coon.commit()
        cursor.close()
        coon.close()
    except:
        print('MYSQL连接处理异常')

    messge = StringIO()
    messge.write('24H用例执行情况!：\n')
#((1, "限价买单不成交"), (2, "限价买单成交"), (3, "市价买单成交"), (4, "限价卖单不成交"), (5, "限价卖单成交"), (6, "市价卖单成交"))
    for reuslt in info:
        if reuslt[0]==1:
            messge.write("限价买单不成交：通过数：{}，失败数：{}".format(reuslt[1], reuslt[2]) + '\n')
        elif reuslt[0]==2:
            messge.write("限价买单成交  ：通过数：{}，失败数：{}".format(reuslt[1], reuslt[2]) + '\n')
        elif reuslt[0]==3:
            messge.write("市价买单成交  ：通过数：{}，失败数：{}".format(reuslt[1], reuslt[2]) + '\n')
        elif reuslt[0]==4:
            messge.write("限价卖单不成交：通过数：{}，失败数：{}".format(reuslt[1], reuslt[2]) + '\n')
        elif reuslt[0]==5:
            messge.write("限价卖单成交  ：通过数：{}，失败数：{}".format(reuslt[1], reuslt[2]) + '\n')
        elif reuslt[0]==6:
            messge.write("市价卖单成交  ：通过数：{}，失败数：{}".format(reuslt[1], reuslt[2]) + '\n')
        else:
            print('erro')

    if len(info):
        dingTalk(messge.getvalue())
    return HttpResponse('ok')
