from django.shortcuts import render, get_object_or_404, redirect
from django.http import (
    HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound,
    HttpResponseServerError,HttpResponse,
)
from django.contrib.staticfiles.storage import staticfiles_storage
import csv
from django.template import Context, Engine, TemplateDoesNotExist, loader
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.http import require_GET

# CSV 読み込み
a = {}
i = 0
file = staticfiles_storage.path('data/youtuber.csv')
csvfile = open(file)
for row in csv.reader(csvfile):
    key_name = "data" + str(i) 
    a[key_name] = row
    i += 1

channelIDs = a['data0']
titles = a['data1']
subscribers = a['data2']
descriptions = a['data3']
videoIDs = a['data4']
video_img = a['data5']
read_items_range = list(range(0, len(channelIDs), 1))
readed_video_number = len(channelIDs)

# Create your views here.
def youtuber(request):
    data_list = zip(channelIDs, titles, subscribers, descriptions, videoIDs, video_img, read_items_range)
    print(data_list)
    context = {'data_list':data_list, 'readed_video_number':readed_video_number}
    
    template = 'myapp/detail.html'
    return render(request, template, context)
