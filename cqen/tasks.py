# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from celery import shared_task
import datetime
import paramiko, time
import getpass, os
import telnetlib
from cqen.models import Nethost, Tasks, Floder

nowTime = datetime.datetime.today().strftime("%Y%m%d")


@shared_task()
def start_ssh_job(cmd):
    for i in cmd:
        print('-----job_start------')
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=i[0], port=i[1], username=i[2], password=i[3])
    try:

        stdin, stdout, stderr = client.exec_command(i[4])
        # time.sleep(3)
        res = stdout.read()
        basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = (os.path.join(basedir, 'media', i[5]))
        print(path + '/' + nowTime + '.log')
        filename = (nowTime + '.log')
        file = open(path + '/' + nowTime + '.log', 'a')
        file.write(res.decode('utf-8', 'ignore'))
        file.flush()
        file.close()
        cmd = 'du -sh' +'\t'+ path + '/' + nowTime + '.log'
        print(cmd)
        stdin, stdout, stderr = client.exec_command(cmd)
        f = stdout.read()
        fsize=str(f,encoding='utf-8')
        ff=fsize[0:4]
        print(ff)
        Floder.objects.filter(folderame=i[5]).update(filename=filename, fpath='/media/',filesize=ff)
        sres = str(res, encoding='utf-8')
        print(sres)
    except Exception as e:
        print(e)
        client.close()
    return {'sshresult': sres}


@shared_task()
def telnet_task_job(host, port, username, passwd, cmd):
    try:
        tn = telnetlib.Telnet(host=host, port=port)
        tn.set_debuglevel(2)
        tn.write(username.encode('ascii') + b"\n")
        tn.write(passwd + '\n')
        if passwd:
            tn.write(passwd.encode('ascii') + b"\n")
            tn.write(cmd + "\n")
            tn.write(exit + "\n")
            sres = tn.read_all().decode('utf-8')
            tn.close()
    except Exception as error:
        print(error)
    return {'telnetresult': sres}
