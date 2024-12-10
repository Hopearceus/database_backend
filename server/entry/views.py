import json
import os

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from .models import Entry
from trip.models import Trip, Trip_Person
from .forms import EntryForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# @login_required
def entry_creation(request, tid):
    if request.method == 'POST':
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.tid = tid
            entry.time = timezone.now()

            # dfa_filter = DFAFilter()
            # filtered_place, has_sensitive_word_place = dfa_filter.filter(entry.place)
            # filtered_desc, has_sensitive_word_desc = dfa_filter.filter(entry.description)

            # if has_sensitive_word_place or has_sensitive_word_desc:
            #     return JsonResponse({
            #         'success': False,
            #         'message': '描述或备注中包含敏感词，请修改后再提交。'
            #     })
            
            # entry.place = filtered_place
            # entry.description = filtered_desc
            entry.save()
            form.save_m2m()

            return JsonResponse({
                'success': True,
                'message': "记录创建成功",
                'redirect_url': reverse('entry_detail', kwargs={'eid': entry.eid})
            })
        else:
            return JsonResponse({
                'success': False,
                'message': '表单数据无效，请检查后重新提交。'
            })
    else:
        return JsonResponse({
                'success': False,
                'message': '表单数据无效，请检查后重新提交。'
            })

# @login_required
def entry_deletion(request, eid):
    entry = get_object_or_404(Entry, eid=eid)
    if request.method == 'POST':
        trip = get_object_or_404(Trip, tid=entry.tid)
        if trip.creator == request.person.pid:
            entry.delete()
            return JsonResponse({
                'success': True,
                'message': "记录已删除"
            })
        else:
            return JsonResponse({
                'success': False,
                'message': "你没有权限删除此记录"
            })
    return JsonResponse({'success': False, 'message': '请求无效'})

# @login_required
def entry_detail(request, eid):
    entry = get_object_or_404(Entry, eid=eid)
    
    if not Trip_Person.objects.filter(tid=entry.tid, pid=request.person.pid).exists():
        return JsonResponse({
            'success': False,
            'message': '你没有权限查看此记录'
        })

    entry_data = {
        'eid': entry.eid,
        'place': entry.place,
        'description': entry.description,
        'time': entry.time.strftime('%Y-%m-%d %H:%M:%S'),  # 转换时间为字符串
        'tid': entry.tid,
    }
    return JsonResponse({
        'success': True,
        'entry': entry_data
    })

# @login_required
def entry_modification(request, eid):
    entry = get_object_or_404(Entry, eid=eid)
    if request.method == 'POST':
        if not Trip_Person.objects.filter(tid=entry.tid, pid=request.person.pid).exists():
            return JsonResponse({
                'success': False,
                'message': "你没有权限修改此记录"
            })

        place = request.POST.get('place', '')
        description = request.POST.get('description', '')

        updated_fields = []
        if place != '':
            entry.place = place
            updated_fields.append('place')
        
        if description != '':
            entry.description = description
            updated_fields.append('description')

        entry.save()

        return JsonResponse({
            'success': True,
            'message': "成功修改entry信息！",
            'updated_fields': updated_fields
        })
    else:
        return JsonResponse({
            'success': False,
            'message': "无效请求！"
        })
