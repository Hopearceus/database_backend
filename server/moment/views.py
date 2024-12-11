import os
import json

from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.core.files.storage import FileSystemStorage
from .models import Moment, Moment_Person
# from .forms import MomentForm
from picture.models import Picture, Picture_Moment, Picture_Album
from person.models import Person
from album.models import Album
from trip.models import Trip
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import jwt

import settings
media_root = settings.MEDIA_ROOT
base_url = settings.base_url
SECRET_KEY = json.loads(open('../key.private').read())['SECRET_KEY']

# @login_required
def moment_add_picture(request, mid, pid):
    pm = Picture_Moment.objects.create(mid=mid, pid=pid)
    pm.save()
    
    return JsonResponse({
        'success': True,
        'message': '图片已添加到圈子',
        'redirect_url': reverse('moment_detail', kwargs={'mid': mid})
    })


# @login_required
def get_discover_moments(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            page = data.get('page', 1)
            page_size = data.get('page_size', 10)
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        moments = Moment.objects.all().order_by('-time')[page_size * (page - 1):page_size * page]
        moments_data = [
            {
                'mid': moment.mid,
                'username': moment.creator.username,
                'userId': moment.creator.pid,
                'content': moment.content,
                'createTime': moment.time.strftime('%Y-%m-%d %H:%M:%S'),
                'tid': moment.tid.tid if moment.tid else None,
            }
            for moment in moments
        ]

        return JsonResponse({'code': 0, 'message': '获取成功', 'data': {'moments': moments_data}})
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @login_required
def get_comments(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mid = data.get('mid')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        comments = Moment_Person.objects.filter(mid=mid, content__isnull=False).values('id', 'content', 'pid__username', 'time')
        return JsonResponse({'code': 0, 'message': '获取成功', 'data': {'comments': list(comments)}})
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @login_required
def add_comment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mid = data.get('mid')
            content = data.get('content')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        moment = get_object_or_404(Moment, mid=mid)
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        comment = Moment_Person.objects.create(mid=moment, pid=person, content=content, time=timezone.now())
        return JsonResponse({'code': 0, 'message': '评论添加成功', 'data': {'id': comment.id}})
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @login_required
def delete_comment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            id = data.get('id')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        comment = get_object_or_404(Moment_Person, id=id, content__isnull=False)
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        if comment.pid.pid == person.pid:
            comment.delete()
            return JsonResponse({'code': 0, 'message': '评论已删除'})
        else:
            return JsonResponse({'code': 403, 'message': '你没有权限删除此评论'}, status=403)
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @login_required
def add_moment(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        tid = request.POST.get('tid')
        
        from person.models import Person
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        
        aid = request.POST.get('aid') if request.POST.get('aid') else person.default_aid
        aid = get_object_or_404(Album, aid=aid)

        if tid:
            tid = get_object_or_404(Trip, tid=tid)
            moment = Moment.objects.create(creator=person, tid=tid, aid=aid, time=timezone.now(), content=content)
        else:
            moment = Moment.objects.create(creator=person, aid=aid, time=timezone.now(), content=content)
        
        images = request.FILES.getlist('images')
        for image in images:
            picture_name = FileSystemStorage(location=os.path.join(media_root, username, 'album/', aid.name)).save(image.name, image)
            picture_url = base_url + settings.MEDIA_URL + username + '/album/' + aid.name + '/' + picture_name
            picture = Picture.objects.create(creator=person, url=picture_url, file_name=picture_name, create_time=timezone.now())
            picture_moment = Picture_Moment.objects.create(pid=picture, mid=moment)
            picture_album = Picture_Album.objects.create(pid=picture, aid=aid)
        
        return JsonResponse({'code': 0, 'message': '动态发表成功', 'data': {'mid': moment.mid}})
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @login_required
def delete_moment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mid = data.get('mid')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '不是有效的 JSON 字符串'}, status=400)

        moment = get_object_or_404(Moment, mid=mid)
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        if moment.creator.pid == person.pid:
            moment.delete()
            return JsonResponse({'code': 0, 'message': '动态已删除'})
        else:
            return JsonResponse({'code': 403, 'message': '你没有权限删除此动态'}, status=403)
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @login_required
def get_moments(request):
    if request.method == 'POST':
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        moments = Moment.objects.filter(creator=person)
        # images = Picture_Moment.objects.filter(mid__in=[moment for moment in moments]).values('pid')
        # images = Picture.objects.filter(pid__in=[image for image in images]).values('url')
        moment_list = []
        for moment in moments:
            images = Picture_Moment.objects.filter(mid=moment.mid)
            images = Picture.objects.filter(pid__in=images.values('pid'))
            moment_list.append({
                'mid': moment.mid,
                'content': moment.content,
                'createTime': moment.time.strftime('%Y-%m-%d %H:%M:%S'),
                'tripId': moment.tid.tid if moment.tid else None,
                'tripName': moment.tid.name if moment.tid else None,
                'userId': moment.creator.pid,
                'username': moment.creator.username,
                'userAvatar': moment.creator.avatar_url,
                'albumId': moment.aid.aid,
                'albumName': moment.aid.name,
                'images': [image.url for image in images]
            })
        return JsonResponse({'code': 0, 'message': '获取成功', 'data': {'moments': moment_list}})
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @login_required
def get_moment_detail(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            mid = data.get('mid')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        moment = get_object_or_404(Moment, mid=mid)
        images = Picture_Moment.objects.filter(mid=moment.mid)
        images = Picture.objects.filter(pid__in=images.values('pid'))
        moment_data = {
            'mid': moment.mid,
            'content': moment.content,
            'createTime': moment.time.strftime('%Y-%m-%d %H:%M:%S'),
            'tripId': moment.tid.tid if moment.tid else None,
            'tripName': moment.tid.name if moment.tid else None,
            'userId': moment.creator.pid,
            'username': moment.creator.username,
            'userAvatar': moment.creator.avatar_url,
            'albumId': moment.aid.aid,
            'albumName': moment.aid.name,
            'images': [image.url for image in images]
        }
        return JsonResponse({'code': 0, 'message': '获取成功', 'data': moment_data})
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)