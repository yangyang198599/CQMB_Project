# -*- coding: utf-8 -*-
from cqen import tasks
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from cqen.models import Tasks
from celery.result import AsyncResult
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django_celery_results.models import TaskResult
import datetime, time
from django.db.models.aggregates import Count
from celery.states import state
from django.views.decorators.cache import cache_page


@login_required
def celery_call(request):
    if request.method == "POST":
        ids = request.POST.getlist('ids')
        for id in ids:
            host_info = Tasks.objects.filter(id=id)
            res = []
            for i in host_info:
                res.append([i.ip, i.port, i.username, i.passwd, i.taskcmd, i.hostname])
                tid = tasks.start_ssh_job.delay(res)

                # tid = tasks.start_ssh_job(res)
                print(tid)
                update_tasklist(id, tid)
                update_result_hostname(i.hostname, tid)
    return redirect("/moretask/")


def update_result_hostname(hostname, task_id):
    time.sleep(1)
    try:
        TaskResult.objects.filter(task_id=task_id).update(host_name=hostname)
    except Exception as e:
        print(e)
    return


# 获取结果

def update_tasklist(ids, tid):
    res = AsyncResult(id=tid)
    if res.ready():
        print(res.status)

        try:
            Tasks.objects.filter(id=ids).update(task_id=tid, task_status=res.status,
                                                tasktime=datetime.datetime.now())

            return res.status
        except Exception as e:
            print(e)

    Tasks.objects.filter(id=ids).update(task_id=tid, task_status=state('任务与发送成功'),
                                        tasktime=datetime.datetime.now())
    return (res.ready())


@login_required
def task_result_list(request):
    if request.method == "POST":
        taskid = request.POST.get('taskid')
        print(taskid)
        clist = TaskResult.objects.filter(task_id=taskid)
        res = []
        for clist in clist.values():
            id = clist['task_id']
            result = clist['result']
            lis = result.encode('utf-8').decode('unicode_escape')
            datedone = clist['date_done']
            status = clist['status']
            res.append([id, lis, status, datedone])

        paginator = Paginator(res, 6)
        page = request.GET.get("page")
        try:
            contacts = paginator.page(page)

        except PageNotAnInteger:

            contacts = paginator.page(1)
        except EmptyPage:

            contacts = paginator.page(paginator.num_pages)
            return render(request, 'taskhistory.html', {'result': contacts})
    else:
        clist = TaskResult.objects.all().annotate(Count("date_done")).order_by("-date_done")
        res = []
        for clist in clist.values():
            id = clist['task_id']
            result = clist['result']
            lis = result.encode('utf-8').decode('unicode_escape')
            datedone = clist['date_done']
            status = clist['status']
            res.append([id, lis, status, datedone])

        paginator = Paginator(res, 6)
        page = request.GET.get("page")
        try:
            contacts = paginator.page(page)



        except PageNotAnInteger:

            contacts = paginator.page(1)
            print(contacts)

        except EmptyPage:

            contacts = paginator.page(paginator.num_pages)
    return render(request, 'taskhistory.html', {'result': contacts})
