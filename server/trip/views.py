import json
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from person.models import Person
from entry.models import Entry
from .models import Trip, Trip_Person
from .forms import TripForm, Trip_PersonForm
# from sensitive_word_filter import DFAFilter

# @login_required
def trip_detail(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tid = data.get('tid')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        trip = get_object_or_404(Trip, tid=tid)
        if not Trip_Person.objects.filter(tid=tid, pid=request.user).exists():
            return JsonResponse({'code': 403, 'message': '你没有权限查看此行程'}, status=403)

        entry_list = Entry.objects.filter(tid=tid).values('eid', 'title')
        trip_data = {
            'tid': trip.tid,
            'name': trip.name,
            'description': trip.description,
            'entries': list(entry_list)
        }
        return JsonResponse({'code': 0, 'message': '获取成功', 'data': trip_data})
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @csrf_exempt
# @login_required
def create_trip(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            description = data.get('description')
            time = timezone.now()
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        if not name or not description:
            return JsonResponse({'code': 400, 'message': '缺少必填字段'}, status=400)

        trip = Trip.objects.create(name=name, description=description, time=time, creator=request.user)
        Trip_Person.objects.create(tid=trip, pid=request.user, notes='')

        return JsonResponse({'code': 0, 'message': '行程创建成功', 'data': {'tid': trip.tid}})
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @csrf_exempt
# @login_required
def delete_trip(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tid = data.get('tid')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        trip = get_object_or_404(Trip, tid=tid)
        if trip.creator == request.user:
            trip.delete()
            return JsonResponse({'code': 0, 'message': '行程已删除'})
        else:
            return JsonResponse({'code': 403, 'message': '你没有权限删除此行程'}, status=403)
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @login_required
def get_trip_list(request):
    if request.method == 'POST':
        trips = Trip.objects.filter(creator=request.user).values('tid', 'name', 'description', 'time')
        return JsonResponse({'code': 0, 'message': '获取成功', 'data': {'trips': list(trips)}})
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @csrf_exempt
# @login_required
def update_trip(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tid = data.get('tid')
            name = data.get('name')
            description = data.get('description')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        trip = get_object_or_404(Trip, tid=tid)
        if trip.creator == request.user:
            trip.name = name
            trip.description = description
            trip.save()
            return JsonResponse({'code': 0, 'message': '行程更新成功'})
        else:
            return JsonResponse({'code': 403, 'message': '你没有权限更新此行程'}, status=403)
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @csrf_exempt
# @login_required
def add_trip_record(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tid = data.get('tid')
            title = data.get('title')
            description = data.get('description')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        trip = get_object_or_404(Trip, tid=tid)
        if Trip_Person.objects.filter(tid=trip, pid=request.user).exists():
            entry = Entry.objects.create(tid=trip, title=title, description=description, time=timezone.now())
            return JsonResponse({'code': 0, 'message': '记录添加成功', 'data': {'eid': entry.eid}})
        else:
            return JsonResponse({'code': 403, 'message': '你没有权限添加此记录'}, status=403)
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @csrf_exempt
# @login_required
def delete_trip_record(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            eid = data.get('eid')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        entry = get_object_or_404(Entry, eid=eid)
        if entry.tid.creator == request.user:
            entry.delete()
            return JsonResponse({'code': 0, 'message': '记录已删除'})
        else:
            return JsonResponse({'code': 403, 'message': '你没有权限删除此记录'}, status=403)
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @login_required
def get_record_detail(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            eid = data.get('eid')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        entry = get_object_or_404(Entry, eid=eid)
        if Trip_Person.objects.filter(tid=entry.tid, pid=request.user).exists():
            entry_data = {
                'eid': entry.eid,
                'title': entry.title,
                'description': entry.description,
                'time': entry.time.isoformat()
            }
            return JsonResponse({'code': 0, 'message': '获取成功', 'data': entry_data})
        else:
            return JsonResponse({'code': 403, 'message': '你没有权限查看此记录'}, status=403)
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @csrf_exempt
# @login_required
def update_record(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            eid = data.get('eid')
            title = data.get('title')
            description = data.get('description')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        entry = get_object_or_404(Entry, eid=eid)
        if Trip_Person.objects.filter(tid=entry.tid, pid=request.user).exists():
            entry.title = title
            entry.description = description
            entry.save()
            return JsonResponse({'code': 0, 'message': '记录更新成功'})
        else:
            return JsonResponse({'code': 403, 'message': '你没有权限更新此记录'}, status=403)
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)
