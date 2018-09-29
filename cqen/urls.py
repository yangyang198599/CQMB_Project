from django.urls import path
from django.conf.urls import url
from cqen import batchtaskview,log_file_download
from cqen import views,operationlogs
from CQMB_Project.settings import MEDIA_ROOT
from django.views.static import serve
app_name='cqen'
urlpatterns = [
    path('celery_call/', batchtaskview.celery_call,name='calltask'),
    path('task_result_list/', batchtaskview.task_result_list,name='task_result_list'),
    path('',views.login_to_index,name='login'),
    path('logout/', views.logout_to_login, name='logout'),
    path('index/',views.index,name='index'),
    path('hostlist/', views.hostlist, name='hostlist'),
    path('addhost/', views.addhost, name='addhost'),
    path('modifyhost/', views.modifyhost, name='modifyhost'),
    path('addtask/', views.addtask, name='addtask'),
    path('deletehost/', views.deletehost, name='deletehost'),
    path('filemgmt/', views.filemgmt, name='filemgmt'),
    path('mkdir/', views.mkdir, name='mkdir'),
    path('sub_file/', views.sub_file, name='sub_file'),
    path('opretionlog/',operationlogs.loglist, name='opreationlog'),
    path('ssh_task/', views.ssh_task, name='ssh_task'),
    path('moretask/', views.moretask, name='moretask'),
    path('getHostInfo/', views.getHostInfo,name='getHostInfo'),
    path('getext/', views.getext, name='getext'),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

]
