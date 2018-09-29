from __future__ import absolute_import, unicode_literals

# 启动时检测celery文件
from .celery import app as celery_app

__all__ = ['celery_app']