
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 设置Django的环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CQMB_Project.settings')
# backend='redis://localhost:6379/0'
#设置app的默认处理方式,如果不设置默认是rabbitMQ
app = Celery('cqen',
             broker='redis://localhost:6379/0')

#配置前缀
app.config_from_object('django.conf:settings', namespace='CELERY')

#自动扫描app下的tasks文件
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))