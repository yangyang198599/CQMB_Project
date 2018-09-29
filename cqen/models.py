from __future__ import unicode_literals
from django.db import models
from django_celery_results.models import TaskResult
from django.utils import timezone

# Create your models here.
class Account(models.Model):
    id = models.AutoField(primary_key=True)
    a_username = models.CharField(max_length=45)
    a_passwd = models.CharField(max_length=45)
    a_company = models.CharField(max_length=100)
    a_tel = models.CharField(max_length=32)


class Nethost(models.Model):
    id = models.AutoField(primary_key=True)
    m_hostname = models.CharField(max_length=45, null=False, verbose_name='主机名', unique=True)
    m_ip = models.CharField(max_length=45, verbose_name='IP', null=False, unique=True)
    m_port = models.CharField(max_length=30, verbose_name='端口', null=False)
    m_username = models.CharField(max_length=45, verbose_name='用户名', null=False)
    m_passwd = models.CharField(max_length=45, verbose_name='密码', null=False)
    m_company = models.CharField(max_length=45, verbose_name='厂商', null=False)


class OperationLogs(models.Model):
    """操作日志"""
    type = models.CharField(max_length=250, verbose_name="类型")
    content = models.TextField(verbose_name="修改详情", null=False)
    username = models.CharField(max_length=45, verbose_name="用户名", null=False)
    url = models.CharField(max_length=45, verbose_name="操作方法", null=False)
    time = models.DateTimeField(max_length=45, verbose_name="时间", null=False)
    value = models.CharField(max_length=45, verbose_name="cmd", null=True)


class Tasks(models.Model):
    id = models.AutoField(primary_key=True)
    task_id = models.CharField(max_length=60, verbose_name='tsaskid', null=True)
    task_status = models.CharField(max_length=60, verbose_name='task_status', null=True)
    hostname = models.CharField(max_length=45, null=False, verbose_name='主机名')
    ip = models.CharField(max_length=45, verbose_name='IP', null=False)
    port = models.CharField(max_length=30, verbose_name='端口', null=False)
    username = models.CharField(max_length=45, verbose_name='用户名', null=False)
    passwd = models.CharField(max_length=45, verbose_name='密码', null=False)
    taskcmd = models.CharField(max_length=100, verbose_name='cmd', null=False)
    tasktime = models.DateTimeField(max_length=45, verbose_name="时间", null=True)
    company = models.CharField(max_length=45, verbose_name='厂商', null=False)


class DownloadPath(models.Model):
    id = models.AutoField(primary_key=True)
    ppath = models.ForeignKey("Floder",to_field='fpath',on_delete=models.CASCADE)
    filename = models.CharField(max_length=60, unique=True)


class Floder(models.Model):
    id = models.AutoField(primary_key=True)
    owner = models.ForeignKey('Nethost',to_field='m_hostname',on_delete=models.CASCADE)
    folderame = models.CharField(max_length=45, null=False, verbose_name='文件名')
    fpath = models.CharField(max_length=60, default='/home/voip/Projects/CQMB_Project/media/',unique=True )
    modifytime = models.TimeField(default=timezone.now)
    filesize = models.CharField(max_length=60, default=0)

class Sysinfo(models.Model):
    id = models.AutoField(primary_key=True)
    osname=models.CharField(max_length=45, null=False, verbose_name='os')
    cpu = models.CharField(max_length=45, null=False, verbose_name='cpu')
    mem=models.CharField(max_length=45, null=False, verbose_name='mem')
    hdisk=models.CharField(max_length=45, null=False, verbose_name='hdisk')