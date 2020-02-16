from django.shortcuts import render

# Create your views here.
from filtering.processing.harlem import VideoMaker


def upload(request, file):
    ctx = {}
    if request.method == 'POST':
        VideoMaker('path-local').run()

    return render(request, 'upload.html', ctx)