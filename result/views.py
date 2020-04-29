from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from notify.notifyTasks import dayNotify

def notify(result):
    ms = dayNotify()
    return HttpResponse(str(ms))
