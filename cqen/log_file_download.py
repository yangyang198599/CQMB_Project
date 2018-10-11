from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def file_download(request):


    file = open('/home/amarsoft/download/example.tar.gz', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="example.tar.gz"'
    return response

@login_required

def subfile(request):


    pass


