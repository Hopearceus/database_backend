import os
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from .forms import AlbumForm
from .models import Album
from picture.models import Picture, Picture_Album
from person.models import Person
from django.contrib.auth.decorators import login_required
from django.utils import timezone

import jwt
from django.utils import timezone

SECRET_KEY = json.loads(open('../key.private').read())['SECRET_KEY']

# @login_required
def create_album(request):
    if request.method == 'POST':
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)

        data = request.POST
        print(data)
        album_name = data.get('albumName')
        print(album_name)
        description = data.get('description', '')
        trip_id = data.get('tripId')

        if not album_name:
            return JsonResponse({'code': 400, 'message': '缺少必填字段 albumName'}, status=400)

        album = Album.objects.create(pid=person.pid, description=description, time=timezone.now())

        cover_image = request.FILES.get('coverImage')
        if cover_image:
            cover_picture = Picture.objects.create(creator=person.pid, image=cover_image, create_time=timezone.now())
            Picture_Album.objects.create(pid=cover_picture.pid, aid=album.aid)

        photos = request.FILES.getlist('photos')
        for photo in photos:
            picture = Picture.objects.create(creator=person.pid, image=photo, create_time=timezone.now())
            Picture_Album.objects.create(pid=picture.pid, aid=album.aid)

        return JsonResponse({'code': 0, 'message': '相册创建成功', 'data': {'aid': album.aid}})
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @login_required
def get_album_list(request):
    if request.method == 'POST':
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        albums = Album.objects.filter(pid=person.pid).values('aid', 'description', 'time')
        return JsonResponse({'code': 0, 'message': '获取成功', 'data': {'albums': list(albums)}})
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @login_required
def get_album_detail(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            aid = data.get('aid')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        album = get_object_or_404(Album, aid=aid)
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        if album.pid == person.pid:
            album_data = {
                'aid': album.aid,
                'description': album.description,
                'time': album.time.isoformat(),
            }
            return JsonResponse({'code': 0, 'message': '获取成功', 'data': album_data})
        else:
            return JsonResponse({'code': 403, 'message': '你没有权限查看此相册'}, status=403)
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @csrf_exempt
# @login_required
def delete_album(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            aid = data.get('aid')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        album = get_object_or_404(Album, aid=aid)
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        if album.pid == person.pid:
            album.delete()
            return JsonResponse({'code': 0, 'message': '相册已删除'})
        else:
            return JsonResponse({'code': 403, 'message': '你没有权限删除此相册'}, status=403)
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @login_required
def get_album_photos(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            aid = data.get('aid')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        album = get_object_or_404(Album, aid=aid)
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        if album.pid == person.pid:
            photos = Picture_Album.objects.filter(aid=album).values('pid', 'image', 'create_time')
            return JsonResponse({'code': 0, 'message': '获取成功', 'data': {'photos': list(photos)}})
        else:
            return JsonResponse({'code': 403, 'message': '你没有权限查看此相册的照片'}, status=403)
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @csrf_exempt
# @login_required
def update_album(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            aid = data.get('aid')
            description = data.get('description')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        album = get_object_or_404(Album, aid=aid)
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        if album.pid == person.pid:
            album.description = description
            album.save()
            return JsonResponse({'code': 0, 'message': '相册更新成功'})
        else:
            return JsonResponse({'code': 403, 'message': '你没有权限更新此相册'}, status=403)
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @csrf_exempt
# @login_required
def update_photo_description(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pid = data.get('pid')
            description = data.get('description')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        picture = get_object_or_404(Picture, pid=pid)
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        if picture.creator == person.pid:
            picture.description = description
            picture.save()
            return JsonResponse({'code': 0, 'message': '照片描述更新成功'})
        else:
            return JsonResponse({'code': 403, 'message': '你没有权限更新此照片的描述'}, status=403)
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @csrf_exempt
# @login_required
def delete_photo(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pid = data.get('pid')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        picture = get_object_or_404(Picture, pid=pid)
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        if picture.creator == person.pid:
            picture.delete()
            return JsonResponse({'code': 0, 'message': '照片已删除'})
        else:
            return JsonResponse({'code': 403, 'message': '你没有权限删除此照片'}, status=403)
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @csrf_exempt
# @login_required
def upload_photos(request):
    if request.method == 'POST':
        try:
            aid = request.POST.get('aid')
            photos = request.FILES.getlist('photos')
        except KeyError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的'}, status=400)

        album = get_object_or_404(Album, aid=aid)
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        if album.pid == person.pid:
            for photo in photos:
                picture = Picture.objects.create(creator=request.user, image=photo, create_time=timezone.now())
                Picture_Album.objects.create(pid=picture, aid=album)
            return JsonResponse({'code': 0, 'message': '照片上传成功'})
        else:
            return JsonResponse({'code': 403, 'message': '你没有权限上传此相���的照片'}, status=403)
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @csrf_exempt
# @login_required
def move_photo_to_album(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            pid = data.get('pid')
            aid = data.get('aid')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        picture = get_object_or_404(Picture, pid=pid)
        album = get_object_or_404(Album, aid=aid)
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        if picture.creator == person.pid and album.pid == person.pid:
            Picture_Album.objects.filter(pid=picture).delete()
            Picture_Album.objects.create(pid=picture, aid=album)
            return JsonResponse({'code': 0, 'message': '照片已移入相册'})
        else:
            return JsonResponse({'code': 403, 'message': '你没有权限移动此照片'}, status=403)
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)