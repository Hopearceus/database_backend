import json
import os

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden

from .models import Entry
from ..trip.models import Trip, Trip_Person
from .forms import EntryForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from sensitive_word_filter import DFAFilter

@login_required
def entry_creation(request, tid):
    if request.method == 'POST':
        form = EntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.tid = tid
            entry.time = timezone.now

            dfa_filter = DFAFilter()
            filtered_place, has_sensitive_word_place = dfa_filter.filter(entry.place)
            filtered_desc, has_sensitive_word_desc = dfa_filter.filter(entry.description)

            if has_sensitive_word_place or has_sensitive_word_desc:
                return render(request, 'questions/creation.html', {
                    'form': form,
                    'error_message': '描述或备注中包含敏感词，请修改后再提交。'
                })
            
            entry.place = filtered_place
            entry.description = filtered_desc
            entry.save()
            form.save_m2m()

            return redirect('entry_detail', eid=entry.eid)
    else:
        form = EntryForm()
        return render(request, 'entry/creation', {
            'form': form
        })

@login_required
def entry_deletion(request, eid):
    entry = get_object_or_404(Entry, eid=eid)
    if request.method == 'POST':
        trip = get_object_or_404(Trip, tid=entry.eid)
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

@login_required
def entry_detail(request, eid):
    entry = get_object_or_404(Trip, eid=eid)
    if not Trip_Person.objects.filter(tid=entry.tid, pid=request.person.pid).exists():
        return HttpResponseForbidden("You do not have permission to view this entry.")

    return render(request, 'entry/detail.html', {
        'entry': entry
    })

@login_required
def entry_modification(request, eid):
    if request.method == 'POST':
        entry = get_object_or_404(Entry, eid=eid)
        if not Trip_Person.objects.filter(tid=entry.tid, pid=request.person.pid).exists():
            return HttpResponseForbidden("you do not have permission to modify this trip.")
        
        if not request.POST.get('place', '').equals(''):
            entry.place = request.POST.get('place', '')
        
        if not request.POST.get('description', '').equals(''):
            entry.description = request.POST.get('description', '')

        return render(request, 'entry/modification.html', {
            'entry': entry,
            'success': True,
            'message': "成功修改entry信息！"
        })
    else:
        return render(request, 'entry/modification.html', {
            'entry': entry,
            'success': False,
            'message': "无效请求！"
        })