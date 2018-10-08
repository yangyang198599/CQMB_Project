#coding=utf-8

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.aggregates import Count
from cqen.models import Nethost, Tasks,Floder
from cqen.operationlogs import operationlogs
from datetime import datetime
import paramiko
import os
from django_celery_results.models import TaskResult

def warningdevice():
    log=TaskResult.objects.filter(ischecked=False)
    key=[]
    values=[]
    for hinfo in log:

        key.append(hinfo.host_name)
        values.append(str(hinfo.result).encode('utf-8').decode('unicode_escape'))
    whost=dict(zip(key,values))

    print(whost)
    return whost



