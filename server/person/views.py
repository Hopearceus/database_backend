from django.contrib.auth import login, authenticate
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
# from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import path, reverse_lazy
from django.http import JsonResponse
from .models import Person
from django.utils import timezone

import json
import jwt

SECRET_KEY = json.loads(open('../key.private').read())['SECRET_KEY']

def register_view(request):
    if request.method == 'POST':
        # default_aid = request.POST.get('default_aid', '')
        # if not pid or not default_aid:
        #     return JsonResponse({'success': False, 'message': '缺少 pid 或 default_aid 参数'}, status=400)


        # album = Album(pid=pid, aid=default_aid, description='默认相册', time=timezone.now())
        # album.save()
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        if not username or not password or not email:
            return JsonResponse({'code': 400, 'message': '缺少必填字段'}, status=400)
        
        if Person.objects.filter(username=username).exists():
            return JsonResponse({'code': 400, 'message': '用户名已存在'}, status=400)
        
        user = Person.objects.create_user(username=username, email=email, password=password)
        from album.models import Album
        default_album = Album.objects.create(pid=user, description='默认相册', time=timezone.now())
        user.default_aid = default_album.aid
        user.save()
        login(request, user)
        data = {}
        data['username'] = user.username
        data['email'] = user.email
        return JsonResponse({'code': 0, 'message': '注册成功', 'data': data})
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @csrf_exempt
def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        if not username or not password:
            return JsonResponse({'code': 400, 'message': '缺少必填字段'}, status=400)

        person = authenticate(request, username=username, password=password)
        if person is not None:
            login(request, person)
            token = jwt.encode({'username': person.username, 'exp': timezone.now() + timezone.timedelta(hours=1)}, SECRET_KEY, algorithm='HS256')
            data = {
                'token': token,
                'expires': (timezone.now() + timezone.timedelta(hours=1)).isoformat()
            }
            return JsonResponse({'code': 0, 'message': '登录成功', 'data': data})
        else:
            return JsonResponse({'code': 401, 'message': '用户名或密码错误'}, status=401)
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        # logout(request)
        return JsonResponse({'code': 0, 'message': '登出成功'})
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

def fetch_user_account_and_permissions(request):
    person = request.user
    data = {
        'account': {
            'username': person.username,
            'email': person.email,
            'phone': person.phone,
            'description': person.description,
            'birthday': person.birthday,
            'gender': person.gender,
        },
        'permissions': ['permission1', 'permission2'], 
        'role': 'user'
    }
    return JsonResponse({'code': 0, 'message': '获取成功', 'data': data})

from django.contrib.auth.decorators import login_required

def get_user_profile(request):
    if request.method == 'GET':
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return JsonResponse({'code': 400, 'message': '缺少 Authorization 头'}, status=400)

        # person = get_object_or_404(Person, pid=request.user.id)
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        # print(person)
        profile_data = {
            'username': person.username,
            'email': person.email,
            'phone': person.phone,
            'description': person.description,
            'birthday': person.birthday,
            'gender': person.gender,
            'avatar': person.avatar_url if person.avatar_url else None,
        }
        return JsonResponse({'code': 0, 'message': '获取成功', 'data': profile_data})
    elif request.method == 'POST':
        person = get_object_or_404(Person, pid=request.POST.get('pid'))
        profile_data = {
            'username': person.username,
            'email': person.email,
            'phone': person.phone,
            'description': person.description,
            'birthday': person.birthday,
            'gender': person.gender,
            'avatar': person.avatar_url if person.avatar_url else None,
        }
        return JsonResponse({'code': 0, 'message': '获取成功', 'data': profile_data})
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

def update_user_profile(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
            person = get_object_or_404(Person, username=username)
            person.username = data.get('username', person.username)
            person.email = data.get('email', person.email)
            person.phone = data.get('phone', person.phone)
            person.description = data.get('description', person.description)
            person.birthday = data.get('birthday', person.birthday)
            person.gender = data.get('gender', person.gender)
            person.save()
            updated_data = {
                'username': person.username,
                'email': person.email,
                'phone': person.phone,
                'description': person.description,
                'birthday': person.birthday,
                'gender': person.gender,
                'avatar': 'http://' + person.avatar_url if person.avatar_url else None,
            }
            return JsonResponse({'code': 0, 'message': '更新成功', 'data': updated_data})
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

from django.core.files.storage import FileSystemStorage

from picture.models import Picture

import os
import settings
media_root = settings.MEDIA_ROOT
base_url = settings.base_url

def upload_avatar(request):
    
    if request.method == 'POST':
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        avatar = request.FILES.get('avatar')
        avatar_name = FileSystemStorage(location=os.path.join(media_root, username, 'avatar/')).save(avatar.name, avatar)
        avatar_url = base_url + settings.MEDIA_URL + username + '/avatar/' + avatar_name
        Picture.objects.create(creator=person, url=avatar_url, description='头像', create_time=timezone.now(), file_name=avatar_name)
        if avatar:
            person.avatar_url = avatar_url
            person.save()
            return JsonResponse({'code': 0, 'message': '头像上传成功', 'data': {'url': person.avatar_url}})
        else:
            return JsonResponse({'code': 400, 'message': '没有上传头像文件'}, status=400)
    else:
        print("adasd")
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)   

def get_person_id(request):
    if request.method == 'POST':
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        return JsonResponse({'code': 0, 'message': '获取成功', 'data': {'pid': person.pid}})
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)