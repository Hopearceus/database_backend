import json
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from person.models import Person
from entry.models import Entry
from .models import Trip, Trip_Person
# from .forms import TripForm, Trip_PersonForm
# from sensitive_word_filter import DFAFilter

import jwt

SECRET_KEY = SECRET_KEY = json.loads(open('../key.private').read())['SECRET_KEY']
# @login_required
def trip_detail(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tid = data.get('tid')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        trip = get_object_or_404(Trip, tid=tid)
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        if not Trip_Person.objects.filter(tid=tid, pid=person).exists():
            return JsonResponse({'code': 403, 'message': '你没有权限查看此行程'}, status=403)

        # entry_list = Entry.objects.filter(tid=tid).values('eid', 'title')
        trip_data = {
            'tid': trip.tid,
            'tripName': trip.name,
            'description': trip.description,
            'creatorId': trip.creator.pid,
            'creatorName': trip.creator.username,
            'sdate': trip.stime,
            'tdate': trip.ttime
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
            name = data.get('tripName')
            description = data.get('description')
            stime = data.get('sdate')
            ttime = data.get('tdate')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        if not name or not stime or not ttime:
            return JsonResponse({'code': 400, 'message': '缺少必填字段'}, status=400)

        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        trip = Trip.objects.create(name=name, description=description, stime=stime, ttime=ttime, creator=person)
        Trip_Person.objects.create(tid=trip, pid=person, notes='')

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
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        if trip.creator.pid == person.pid:
            trip.delete()
            return JsonResponse({'code': 0, 'message': '行程已删除'})
        else:
            return JsonResponse({'code': 403, 'message': '你没有权限删除此行程'}, status=403)
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @login_required
def get_trip_list(request):
    if request.method == 'POST':
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        trips = Trip.objects.filter(creator=person.pid).values('tid', 'name', 'description', 'stime', 'ttime')
        trip_list = []
        for trip in trips:
            trip_list.append({
                'tid': trip['tid'],
                'tripName': trip['name'],
                'description': trip['description'],
                'sdate': trip['stime'],
                'tdate': trip['ttime'],
                'creatorId': person.pid,
                'creatorName': person.username
            })
        return JsonResponse({'code': 0, 'message': '获取成功', 'data': {'trips': trip_list}})
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

# @csrf_exempt
# @login_required
def update_trip(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            tid = data.get('tid')
            name = data.get('tripName')
            sdate = data.get('sdate')
            tdate = data.get('tdate')
            description = data.get('description')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        trip = get_object_or_404(Trip, tid=tid)
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        if trip.creator.pid == person.pid:
            trip.name = name if name else trip.name
            trip.description = description if description else trip.description
            trip.stime = sdate if sdate else trip.stime
            trip.ttime = tdate if tdate else trip.ttime
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
            # title = data.get('title')
            place = data.get('location')
            time = data.get('recordDate')
            description = data.get('description')
        except json.JSONDecodeError:
            return JsonResponse({'code': 400, 'message': '请求体不是有效的 JSON 字符串'}, status=400)

        trip = get_object_or_404(Trip, tid=tid)
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        if Trip_Person.objects.filter(tid=trip, pid=person.pid).exists():
            entry = Entry.objects.create(tid=trip, place=place, description=description, time=time)
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
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        if entry.tid.creator.pid == person.pid:
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
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        if Trip_Person.objects.filter(tid=entry.tid, pid=person.pid).exists():
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
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)
        if Trip_Person.objects.filter(tid=entry.tid, pid=person.pid).exists():
            entry.title = title
            entry.description = description
            entry.save()
            return JsonResponse({'code': 0, 'message': '记录更新成功'})
        else:
            return JsonResponse({'code': 403, 'message': '你没有权限更新此记录'}, status=403)
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)

def get_record_list(request):
    if request.method == 'POST':
        username = jwt.decode(request.headers['Authorization'].split(' ')[1], SECRET_KEY, algorithms=['HS256'])['username']
        person = get_object_or_404(Person, username=username)

        trip_persons = Trip_Person.objects.filter(pid=person.pid)
        trip_ids = [tp.tid for tp in trip_persons]
        entries = Entry.objects.filter(tid__in=trip_ids)

        record_list = []
        for entry in entries:
            record_data = {
                'title': entry.title,
                'eid': entry.eid,
                'tid': entry.tid.tid,
                'recordDate': entry.time,
                'location': entry.place,
                'description': entry.description,
            }
            record_list.append(record_data)

        return JsonResponse({'code': 200, 'data': {'records': record_list}})
    else:
        return JsonResponse({'code': 405, 'message': '请求方法不允许'}, status=405)