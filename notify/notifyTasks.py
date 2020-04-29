import datetime

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
        messge.write('为了自由！！\n')
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
        messge.write('为了自由！！\n')
        dingTalk(messge.getvalue())
    return messge.getvalue()
