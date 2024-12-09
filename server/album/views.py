import os
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden

from ..moment.models import Moment, Moment_Person
from .forms import AlbumForm
from ..person.models import Person
from .models import Album
from ..picture.models import Picture, Picture_Album
from ..trip.models import Trip, Trip_Person
from django.contrib.auth.decorators import login_required
from sensitive_word_filter import DFAFilter
from django.utils import timezone


@login_required
def album_creation(request):
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album = form.save(commit=False)
            album.pid = request.person.pid
            album.time = timezone.now()
            
            dfa_filter = DFAFilter()
            filtered_desc, has_sensitive_word = dfa_filter(album.description)
            if has_sensitive_word:
                return render(request, 'moment/creation', {
                    'form': form,
                    'message': "存在敏感词，请重试！"
                })
            album.description = filtered_desc
            album.save()
            return redirect('album_detail', mid=album.aid)
    else:
        form = AlbumForm()
        return render(request, 'album/creation.html', {
            'form': form
        })

def album_deletion(request, aid):
    album = get_object_or_404(Album, aid=aid)
    if request.method == 'POST':
        if album.pid == request.person.pid:
            album.delete()
            return JsonResponse({'success': True, 'message': '相册已删除'})
        else:
            return JsonResponse({'success': False, 'message': '你没有权限删除此相册'})
    return JsonResponse({'success': False, 'message': '请求无效'})

def album_detail(request, aid):
    album = get_object_or_404(Album, id=aid)
    # return render(request, 'album/detail.html', {
    #     'album': album
    # })
    return JsonResponse({'album': {_ for _ in album}})

def album_add_picture(request, aid, picture_id):
    album = get_object_or_404(Album, aid=aid, pid=request.person.pid)
    if request.method == 'POST':
        try:
            picture_album = Picture_Album.objects.filter(pid=picture_id, aid=aid)
        except Picture_Album.DoesNotExist:
            picture_album = Picture_Album(pid=picture_id, aid=aid)
            picture_album.save()
    # return redirect('album_detail', aid=album.id)
    return JsonResponse({'success': True})