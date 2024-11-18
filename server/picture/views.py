import os
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden

from ..moment.models import Moment, Moment_Person
from .forms import PictureForm
from ..person.models import Person
from .models import Picture, Picture_Album
from ..trip.models import Trip, Trip_Person
from django.contrib.auth.decorators import login_required
from sensitive_word_filter import DFAFilter
from django.utils import timezone

@login_required
def picture_upload(request):
    if request.method == 'POST':
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.save(commit=False)
            picture.creator = request.person.pid
            picture.create_time = timezone.now()
            picture.save()
            picture_album = Picture_Album(pid=picture.pid, aid=request.person.default_aid, moved_time=timezone.now())
            picture_album.save()
            return redirect('detail')
    else:
        form = PictureForm()
        return render(request, 'picture/creation', {
            'form': form
        })

def picture_deletion(request, picture_id):
    picture = get_object_or_404(Picture, pid=picture_id)
    if request.method == 'POST':
        if picture.creator == request.person.pid:
            picture_upload.delete()
            return JsonResponse({'success': True, 'message': '照片已删除'})
        else:
            return JsonResponse({'success': False, 'message': '你没有权限删除此照片'})
    return JsonResponse({'success': False, 'message': '请求无效'})

def picture_detail(request, picture_id):
    picture = get_object_or_404(Picture, pid=picture_id)
    return render(request, 'picture/detail', {
        'picture': picture
    })