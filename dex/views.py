from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from dex.tasks import DexTest


def rundextest(request):
    DexTest('XT').runTest()
    DexTest('WICC').runTest()
    return HttpResponse('OK')