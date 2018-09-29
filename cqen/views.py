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




# 登陆
def login_to_index(request):
    if request.method == "POST":

        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        if user is None:
            status = {'error': '用户名或密码错误'}
            return render(request, "login.html", status)

        else:
            login(request, user)
            return redirect("index/")

    return render(request, "login.html")


@login_required
# 首页
def index(request):
    list = Nethost.objects.values('m_company').distinct().annotate(Count('id'))
    return render(request, 'index.html', {'list': list})


def logout_to_login(request):
    logout(request)
    return redirect('cqen:login')


@login_required
def hostlist(request):
    # contact_list = Nethost.objects.all().order_by("id")
    contact_list = Nethost.objects.all().annotate(Count("m_hostname")).order_by("m_hostname")
    print(contact_list)
    paginator = Paginator(contact_list, 12, 3)
    page = request.GET.get("page")
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:

        contacts = paginator.page(1)
    except EmptyPage:

        contacts = paginator.page(paginator.num_pages)

    return render(request, 'hostlist.html', {'hostinfo': contacts})


@accept_websocket
def ssh_task(request):
    clientip = request.GET.get('inputip')
    print(clientip)
    if request.is_websocket():

        clients = request.websocket

        for client in clients:
            strs = str(client, encoding='utf-8')
            dd = strs.split('|', strs.__len__())
            print(dd[0])

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=dd[1], port=dd[2], username=dd[3], password=dd[4])
            if dd[1] is None:
                return
            try:
                stdin, stdout, stderr = ssh.exec_command(dd[0])
                # time.sleep(0.2)
                res = stdout.read()
                print(res)
                clients.send(res)
                ssh.close()
                sshlog(request, dd[0])
            except Exception as e:
                print(e)

    return render(request, "ssh_task.html")


@login_required
def addtask(request):
    sucess = {'sucess': '添加成功'}
    error = {'error': '添加失败'}
    if request.method == "POST":
        hostname = request.POST.get('hostname')
        ip = request.POST.get('ip')

        port = request.POST.get('port')
        username = request.POST.get('username')
        passwd = request.POST.get('passwd')
        company = request.POST.get('company')
        taskcmd = request.POST.get('taskcmd')
    try:
        task = Tasks.objects.create(hostname=hostname, ip=ip, port=port, username=username, passwd=passwd,
                                    company=company, taskcmd=taskcmd)
        task.save()
        return render(request, "addtask.html", sucess)
    except Exception as e:
        print(e)

        return render(request, "addtask.html", error)

    return render(request, 'addtask.html')


@login_required
def addhost(request):
    sucess = {'sucess': '添加主机成功'}
    error = {'error': '添加主机失败'}
    type=['添加主机','修改主机']
    if request.method == "POST":
        id = request.POST.get('id')
        m_hostname = request.POST.get('hostname')
        m_ip = request.POST.get('ip')
        m_port = request.POST.get('port')
        m_username = request.POST.get('username')
        m_passwd = request.POST.get('passwd')
        m_company = request.POST.get('company')
        modif = request.POST.get('modfiy')
        if modif is None:
            try:
                cnethost = Nethost.objects.create(m_hostname=m_hostname, m_ip=m_ip, m_port=m_port, m_username=m_username,
                                                 m_passwd=m_passwd, m_company=m_company)
                cnethost.save()
                logrecode(request,type[0])
                return  redirect('/hostlist')
            except:
                return   redirect('/hostlist')
        else:
            Nethost.objects.filter(id=id).update(m_hostname=m_hostname, m_ip=m_ip, m_port=m_port, m_username=m_username,m_passwd=m_passwd, m_company=m_company)
            logrecode(request, type[1])
            return redirect('/hostlist')
    return render(request,"addhost.html")


@login_required
def deletehost(request):
    error = {'error': '失败'}
    if request.method == 'POST':
        ids = request.POST.getlist('ids')
        for id in ids:
            try:
                nethost = Nethost.objects.filter(id=id).delete()
                print(nethost[0])
                if nethost[0] == 1:
                    logrecode(request,'删除主机')
                else:
                    return JsonResponse(error)
            except Exception as e:
                print(e)
                return JsonResponse(error)
    return redirect('/hostlist')


@login_required
def modifyhost(request):
    error = {'error': '失败'}
    if request.method == "POST":
        ids = request.POST.get('ids')
        host = Nethost.objects.filter(id=ids)
        return render(request, "modifyhost.html", {'hostinfo': host})
    else:
        return render(request, "modifyhost.html", error)
    return redirect('/hostlist')


def logrecode(request,type):
    user = request.user.username

    cmd = request.get_full_path_info()
    print(cmd)
    if type=='添加主机':
        operationlogs(sdate=datetime.now(), url=cmd, username=user, value='操作成功', type=type)
    if type=='修改主机':
        operationlogs(sdate=datetime.now(), url=cmd, username=user, value='操作成功', type=type)
    if type=='删除主机':
        operationlogs(sdate=datetime.now(), url=cmd, username=user, value='操作成功', type=type)
    return True


def sshlog(request, cmd):
    data = request.GET.get('inputip')
    user = request.user.username
    print(data)
    cmds = cmd
    print(cmds)
    if data is None:
        operationlogs(sdate=datetime.now(), url='shell命令', username=user, value=cmds, type='shell command')
    if data is not None:
        operationlogs(sdate=datetime.now(), url=data, username=user, value=cmds, type='shell')
    return True


@login_required
def getHostInfo(request):
    hostinfo = Nethost.objects.filter(m_hostname__isnull=False)
    res = []
    for i in hostinfo:
        res.append([i.id, i.m_hostname, i.m_ip, i.m_port, i.m_username, i.m_passwd])
    print(res)
    return JsonResponse({'hostinfo': res})


@login_required
def getext(request):
    hostinfo = Nethost.objects.filter(id=request.GET.get('id'))
    res = []
    for i in hostinfo:
        res.append([i.id, i.m_hostname, i.m_ip, i.m_port, i.m_username, i.m_passwd])
    print(res)
    return JsonResponse({'textinfo': res})


@login_required
def moretask(request):
    contact_list = Tasks.objects.all().annotate(Count("tasktime")).order_by("-tasktime")
    paginator = Paginator(contact_list, 10)
    page = request.GET.get("page")
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:

        contacts = paginator.page(1)
    except EmptyPage:

        contacts = paginator.page(paginator.num_pages)
    return render(request, 'tasklist.html', {'tasklist': contacts})


def filemgmt(request):

        contact_list = Floder.objects.all()
        paginator = Paginator(contact_list, 5)
        page = request.GET.get("page")
        try:
           contacts = paginator.page(page)
        except PageNotAnInteger:

           contacts = paginator.page(1)
        except EmptyPage:

           contacts = paginator.page(paginator.num_pages)
        return render(request, "file.html", {'floderlist': contacts})


@login_required
def sub_file(request):

    return  render(request,"sub_file.html")

@login_required
def mkdir(request):
    error = {'error': '文件夹已存在'}
    if request.method == 'POST':
        flodername = request.POST.get('foldername')
        basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = (os.path.join(basedir, 'media', flodername))
        print(path)
        if not os.path.exists(path):
            os.makedirs(path)
            Floder.objects.create(owner_id=flodername, fpath=path, folderame=flodername)
            return redirect("/filemgmt")

        else:
            return render(request, "file.html", error)
    return render(request, "file.html")
