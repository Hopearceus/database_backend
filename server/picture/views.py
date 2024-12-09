import os
import json

from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from ..moment.models import Moment, Moment_Person
from .forms import PictureForm
from ..person.models import Person
from .models import Picture, Picture_Album
from ..trip.models import Trip, Trip_Person
from sensitive_word_filter import DFAFilter

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

            return JsonResponse({
                'success': True,
                'message': '照片上传成功',
                'picture': {
                    'pid': picture.pid,
                    'url': picture.image.url,
                    'create_time': picture.create_time.strftime('%Y-%m-%d %H:%M:%S')
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'message': '表单无效',
                'errors': form.errors
            }, status=400)
    else:
        return JsonResponse({
            'success': False,
            'message': '无效请求，必须使用 POST 方法'
        }, status=405)


def picture_deletion(request, picture_id):
    picture = get_object_or_404(Picture, pid=picture_id)
    if request.method == 'POST':
        if picture.creator == request.person.pid:
            picture.delete()
            return JsonResponse({
                'success': True,
                'message': '照片已删除'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': '你没有权限删除此照片'
            })
    return JsonResponse({
        'success': False,
        'message': '请求无效'
    }, status=400)


def picture_detail(request, picture_id):
    picture = get_object_or_404(Picture, pid=picture_id)
    picture_data = {
        'pid': picture.pid,
        'url': picture.image.url,
        'creator': picture.creator,
        'create_time': picture.create_time.strftime('%Y-%m-%d %H:%M:%S'),
    }

    return JsonResponse({
        'success': True,
        'picture': picture_data
    })
