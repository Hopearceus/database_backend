import os
import json

from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from .models import Moment, Moment_Person
from .forms import MomentForm
from picture.models import Picture, Picture_Moment
from person.models import Person
from trip.models import Trip
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import jwt

SECRET_KEY = json.loads(open('../key.private').read())['SECRET_KEY']

# @login_required
def moment_add_picture(request, mid, pid):
    pm = Picture_Moment(mid=mid, pid=pid)
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
                'creator': moment.creator.username,
                'text': moment.text,
                'time': moment.time.isoformat(),
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
        comment = Moment_Person.objects.create(mid=moment, pid=person.pid, content=content, time=timezone.now())
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
        if comment.pid == person.pid:
            comment.delete()
            return JsonResponse({'code': 0, 'message': '评论已删除'})
        else:
            return JsonResponse({'code': 403, 'message': '你没有权限删除此评论'}, status=403)
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @login_required
def add_moment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            content = data.get('content')
            tid = data.get('tid')
            aid = data.get('aid')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        moment = Moment.objects.create(creator=person.pid, text=content, tid_id=tid, aid_id=aid, time=timezone.now())
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
            return JsonResponse({'code': 400, 'message': '��求体不是有效的 JSON 字符串'}, status=400)

        moment = get_object_or_404(Moment, mid=mid)
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        if moment.creator == person.pid:
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
        # moments = Moment.objects.filter(creator=person.pid).values('mid', 'text', 'time', 'tid', 'aid')
        moments = Moment.objects.filter(creator=person.pid).values('mid', 'text', 'time', 'tid')
        return JsonResponse({'code': 0, 'message': '获取成功', 'data': {'moments': list(moments)}})
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
        moment_data = {
            'mid': moment.mid,
            'text': moment.text,
            'creator': moment.creator.username,
            'time': moment.time.isoformat(),
            'tid': moment.tid.tid if moment.tid else None,
            'aid': moment.aid.aid if moment.aid else None,
        }
        return JsonResponse({'code': 0, 'message': '获取成功', 'data': moment_data})
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)