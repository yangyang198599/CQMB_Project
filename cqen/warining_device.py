from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.aggregates import Count
from cqen.models import Nethost, Tasks,Floder
from cqen.operationlogs import operationlogs
from datetime import datetime
from dwebsocket import accept_websocket
import paramiko
import os
from django_celery_results.models import TaskResult

def warning(request):
    task_id=Tasks.objects.filter(task_id__isnull=False)
    warninglog=TaskResult.objects.filter(ischecked=0)
    print(warninglog)
    pass

