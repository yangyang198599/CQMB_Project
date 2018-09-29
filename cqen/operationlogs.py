from cqen.models import OperationLogs
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def operationlogs(sdate, url, username, value, type):
    try:
        recode = OperationLogs.objects.create(time=sdate, url=url, username=username, value=value, type=type)
    except Exception as e:
        print(e)
        return False


@login_required
def loglist(request):
    contact_list = OperationLogs.objects.all().order_by("-id")
    paginator = Paginator(contact_list, 12)
    page = request.GET.get("page")
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:

        contacts = paginator.page(1)
    except EmptyPage:

        contacts = paginator.page(paginator.num_pages)

    return render(request, 'operetionlog.html', {'loginfo': contacts})
