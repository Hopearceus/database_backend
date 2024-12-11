import os
import json

from django.core.files.storage import FileSystemStorage
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
import os

import settings
media_root = settings.MEDIA_ROOT
base_url = settings.base_url

SECRET_KEY = json.loads(open('../key.private').read())['SECRET_KEY']

# @login_required
def create_album(request):
    if request.method == 'POST':
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        
        album_name = request.POST.get('albumName')
        description = request.POST.get('description', '')
        trip_id = request.POST.get('tripId')

        if not album_name:
            return JsonResponse({'code': 400, 'message': '缺少必填字段 albumName'}, status=400)

        album = Album.objects.create(pid=person, name=album_name, description=description, time=timezone.now())
        
        cover_image = request.FILES.get('coverImage')
        if cover_image:
            cover_name = FileSystemStorage(location=os.path.join(media_root, username, 'album/', album.name)).save(cover_image.name, cover_image)
            cover_url = base_url + settings.MEDIA_URL + username + '/album/' + album.name + '/' + cover_name
            cover_picture = Picture.objects.create(creator=person, url=cover_url, file_name=cover_name, create_time=timezone.now())
            Picture_Album.objects.create(pid=cover_picture, aid=album)
            album.cover_url = cover_url
            album.save()
        photos = request.FILES.getlist('photos')
        for photo in photos:
            photo_name = FileSystemStorage(location=os.path.join(media_root, username, 'album/', album.name)).save(photo.name, photo)
            photo_url = base_url + settings.MEDIA_URL + username + '/album/' + album.name + '/' + photo_name
            picture = Picture.objects.create(creator=person, url=photo_url, file_name=photo_name, create_time=timezone.now())
            Picture_Album.objects.create(pid=picture, aid=album)

        return JsonResponse({'code': 0, 'message': '相册创建成功', 'data': {'aid': album.aid}})
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @login_required
def get_album_list(request):
    if request.method == 'GET':
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        albums = Album.objects.filter(pid=person.pid)

        album_list = []
        for album in albums:
            photo_count = Picture_Album.objects.filter(aid=album.aid).count()
            album_data = {
                'aid': album.aid,
                'albumName': album.name,
                'description': album.description,
                'coverUrl': album.cover_url,
                'photoCount': photo_count,
                'createdAt': album.time.strftime('%Y-%m-%d %H:%M:%S'),
                'creatorId': album.pid.pid,
                'creatorName': album.pid.username
            }
            album_list.append(album_data)
        return JsonResponse({'code': 200, 'data': {'albums': album_list}})
    elif request.method == 'POST':
        data = json.loads(request.body)
        pid = data.get('pid')
        person = get_object_or_404(Person, pid=pid)
        albums = Album.objects.filter(pid=person.pid)

        album_list = []
        for album in albums:
            photo_count = Picture_Album.objects.filter(aid=album.aid).count()
            album_data = {
                'aid': album.aid,
                'albumName': album.name,
                'description': album.description,
                'coverUrl': album.cover_url,
                'photoCount': photo_count,
                'createdAt': album.time.strftime('%Y-%m-%d %H:%M:%S'),
                'creatorId': album.pid.pid,
                'creatorName': album.pid.username
            }
            album_list.append(album_data)
        return JsonResponse({'code': 200, 'data': {'albums': album_list}})
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
        photo_count = Picture_Album.objects.filter(aid=album.aid).count()
        album_data = {
            'aid': album.aid,
            'albumName': album.name,
            'description': album.description,
            'coverUrl': album.cover_url,
            'photoCount': photo_count,
            'createdAt': album.time.strftime('%Y-%m-%d %H:%M:%S'),
            'creatorId': person.pid,
            'creatorName': person.username
        }
        return JsonResponse({'code': 0, 'message': '获取成功', 'data': album_data})
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
        if album.pid.pid == person.pid:
            if album.aid == person.default_aid:
                return JsonResponse({'code': 114514, 'message': '默认相册不允许删除', 'data': {'code': 1}}, status=403)
            album.delete()
            return JsonResponse({'code': 0, 'message': '相册已删除', 'data': {'code': 0}})
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
        # username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        # person = get_object_or_404(Person, username=username)
        photos = Picture_Album.objects.filter(aid=album).values('pid')
        photos = Picture.objects.filter(pid__in=photos)
        photo_list = []
        for photo in photos:
            photo_data = {
                'pid': photo.pid,
                'url': photo.url,
                'uploadTime': photo.create_time.strftime('%Y-%m-%d %H:%M:%S'),
                'description': photo.description
            }
            photo_list.append(photo_data)
        return JsonResponse({'code': 0, 'message': '获取成功', 'data': {'photos': photo_list}})
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
            name = data.get('albumName')
            
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        album = get_object_or_404(Album, aid=aid)
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        if album.pid.pid == person.pid:
            album.description = description
            album.name = name
            album.save()
            photo_count = Picture_Album.objects.filter(aid=album).count()
            album_data = {
                'aid': album.aid,
                'albumName': album.name,
                'description': album.description,
                'coverUrl': album.cover_url,
                'photoCount': photo_count,
                'createdAt': album.time.strftime('%Y-%m-%d %H:%M:%S'),
                'creatorId': person.pid,
                'creatorName': person.username
            }
            return JsonResponse({'code': 0, 'message': '相册更新成功', 'data': album_data})
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
        
        if picture.creator.pid == person.pid:
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
        album = Picture_Album.objects.filter(pid=picture).values('aid')
        album = Album.objects.get(aid=album[0]['aid'])
        if picture.creator.pid == person.pid:
            if album.cover_url == picture.url:
                album.cover_url = ''
                album.save()
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
        if album.pid.pid == person.pid:
            for photo in photos:
                photo_name = FileSystemStorage(location=os.path.join(media_root,username,'album/',album.name)).save(photo.name,photo)
                photo_url = base_url + settings.MEDIA_URL + username + '/album/' + album.name + '/' + photo_name
                picture = Picture.objects.create(creator=person, url=photo_url, file_name=photo_name, image=photo, create_time=timezone.now())
                Picture_Album.objects.create(pid=picture, aid=album)
            return JsonResponse({'code': 0, 'message': '照片上传成功'})
        else:
            return JsonResponse({'code': 403, 'message': '你没有权限上传此相册的照片'}, status=403)
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)