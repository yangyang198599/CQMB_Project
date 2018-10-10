# coding=utf-8

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.aggregates import Count
from cqen.models import Nethost, Tasks, Floder
from cqen.operationlogs import operationlogs
from datetime import datetime
import paramiko
import os
from django_celery_results.models import TaskResult


def warningdevice():
    log = TaskResult.objects.filter(ischecked=False)
    key = []
    values = []
    for hinfo in log:
        key.append(hinfo.host_name)
        values.append(str(hinfo.result).encode('utf-8').decode('unicode_escape'))
    whost = dict(zip(key, values))

    print(whost)
    return whost


def deviceischeckd():
    log = TaskResult.objects.filter(ischecked=True)
    key = []
    for hinfo in log:
        key.append(hinfo.host_name)
    keys = list(set(key))
    print(keys)
    return keys


@login_required
def waringchecked(request):
    if request.method == 'POST':
        hostname = request.POST.get('check')
        try:
            TaskResult.objects.filter(host_name=hostname).update(ischecked=True)
        except Exception as e:
            print(e)

    return redirect('cqen:index')
