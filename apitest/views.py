from django.http import HttpResponse
from django.shortcuts import render

# Create your views here
from apitest.run import BaasApi

def runapicase(request):
    baasApi = BaasApi()
    result = baasApi.runAll()
    return HttpResponse(str(result))