import json
import os

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden

from ..person.models import Person
from ..entry.models import Entry
from .models import Trip, Trip_Person
from .forms import TripForm, Trip_PersonForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from sensitive_word_filter import DFAFilter

'''
input:
    request: [optional]search->str, user
return:
    tid_list->list: list of user's trip id
    trip_list->list: list of user's trip
    search_performed: search or not
    search_results: user's trip with 'search' in name
'''
@login_required
def trip_management(request):
    try:
        person = Person.objects.get(user=request.user)
    except Person.DoesNotExist:
        tid_list = []
    else:
        trip_person_set = Trip_Person.objects.filter(pid=person)
        tid_list = list(trip_person_set.values_list('tid', flat=True).distinct())

    search_query = request.GET.get('search', '')
    if search_query:
        search_results = Trip.objects.filter(name__icontains=search_query, tid__in=tid_list)
        search_performed = True
    else:
        search_results = []
        search_performed = False
    
    trip_list = Trip.objects.filter(tid__in=tid_list)

    return render(request, 'trip/management.html',{
        'tid_list': tid_list,
        'trip_list': trip_list,
        'search_performed': search_performed,
        'search_results': search_results
    })

@login_required
def trip_creation(request):
    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.creator = request.user
            trip_person = Trip_Person(tid=trip.tid, pid=trip.creator, notes=request.POST.get('notes', '')).save(commit=False)
            
            
            dfa_filter = DFAFilter()
            filtered_description, has_sensitive_word_desc = dfa_filter.filter(trip.description)
            filtered_notes, has_sensitive_word_notes = dfa_filter.filter(trip_person.notes)

            if has_sensitive_word_desc or has_sensitive_word_notes:
                return render(request, 'questions/creation.html', {
                    'form': form,
                    'error_message': '描述或备注中包含敏感词，请修改后再提交。'
                })
            
            trip.description = filtered_description
            trip_person.notes =  filtered_notes
            trip.save()
            trip_person.save()
            form.save_m2m()

            return redirect('trip_detail', tid=trip.tid)
    else:
        form = TripForm()
        return render(request, 'trip/creation.html', {
            'form': form
        })

@login_required
def trip_deletion(request, tid):
    trip = get_object_or_404(Trip, tid=tid)
    if request.method == 'POST':
        if trip.creator == request.user:
            trip.delete()
            # TODO: 检查trip_person表里面是不是删除了
            return JsonResponse({'success': True, 'message': '行程已删除'})
        else:
            return JsonResponse({'success': False, 'message': '你没有权限删除此行程'})
    return JsonResponse({'success': False, 'message': '请求无效'})

@login_required
def trip_detail(request, tid):
    trip = get_object_or_404(Trip, tid=tid)
    if not Trip_Person.objects.filter(tid=tid, pid=request.person.pid).exists():
        return HttpResponseForbidden("You do not have permission to view this trip.")
    
    entry_list = Entry.objects.filter(tid=tid)

    return render(request, 'trip/detail.html', {
        'trip': trip,
        'entry_list': entry_list
    })

@login_required
def trip_modification_description(request, tid):
    if request.method == 'POST':
        trip = get_object_or_404(Trip, tid=tid)
        if not Trip_Person.objects.filter(tid=tid, pid=request.person.pid).exists():
            return HttpResponseForbidden("you do not have permission to modify this trip.")
        
        trip.description = request.POST.get('description', '')
        trip.save()
        
        return render(request, 'trip/modification/description.html', {
            'trip': trip,
            'success': True
        })
    else:
        return render(request, 'trip/modification/description', {
            'trip': trip,
            'success': False
        })

@login_required
def trip_modification_notes(request, tid):
    if request.method == 'POST':
        trip = get_object_or_404(Trip, tid=tid)
        if not Trip_Person.objects.filter(tid=tid, pid=request.person.pid).exists():
            return HttpResponseForbidden("you do not have permission to modify this trip.")
        
        tp = get_object_or_404(Trip_Person, tid=tid, pid=request.person.pid)
        tp.notes = request.POST.get('notes', '')
        tp.save()
        
        return render(request, 'trip/modification/description.html', {
            'trip': trip,
            'success': True
        })
    else:
        return render(request, 'trip/modification/description', {
            'trip': trip,
            'success': False
        })