import json
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from ..person.models import Person
from ..entry.models import Entry
from .models import Trip, Trip_Person
from .forms import TripForm, Trip_PersonForm
from sensitive_word_filter import DFAFilter


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

    return JsonResponse({
        'success': True,
        'tid_list': tid_list,
        'trip_list': list(trip_list.values('tid', 'name')),
        'search_performed': search_performed,
        'search_results': list(search_results.values('tid', 'name')),
    })


@login_required
def trip_creation(request):
    if request.method == 'POST':
        form = TripForm(request.POST, request.FILES)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.creator = request.user
            trip.save()

            trip_person = Trip_Person(tid=trip.tid, pid=trip.creator, notes=request.POST.get('notes', ''))
            trip_person.save()

            dfa_filter = DFAFilter()
            filtered_description, has_sensitive_word_desc = dfa_filter.filter(trip.description)
            filtered_notes, has_sensitive_word_notes = dfa_filter.filter(trip_person.notes)

            if has_sensitive_word_desc or has_sensitive_word_notes:
                return JsonResponse({
                    'success': False,
                    'message': '描述或备注中包含敏感词，请修改后再提交。'
                })

            trip.description = filtered_description
            trip_person.notes = filtered_notes
            trip.save()
            trip_person.save()

            return JsonResponse({
                'success': True,
                'message': '行程创建成功',
                'trip': {
                    'tid': trip.tid,
                    'name': trip.name,
                    'description': trip.description
                }
            })

        return JsonResponse({
            'success': False,
            'message': '表单无效',
            'errors': form.errors
        }, status=400)

    return JsonResponse({
        'success': False,
        'message': '请求方法不允许'
    }, status=405)


@login_required
def trip_deletion(request, tid):
    trip = get_object_or_404(Trip, tid=tid)
    if request.method == 'POST':
        if trip.creator == request.user:
            trip.delete()
            return JsonResponse({
                'success': True,
                'message': '行程已删除'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': '你没有权限删除此行程'
            })

    return JsonResponse({
        'success': False,
        'message': '请求无效'
    }, status=400)


@login_required
def trip_detail(request, tid):
    trip = get_object_or_404(Trip, tid=tid)
    if not Trip_Person.objects.filter(tid=tid, pid=request.person.pid).exists():
        return JsonResponse({
            'success': False,
            'message': '你没有权限查看此行程'
        }, status=403)
    
    entry_list = Entry.objects.filter(tid=tid).values('eid', 'title')

    return JsonResponse({
        'success': True,
        'trip': {
            'tid': trip.tid,
            'name': trip.name,
            'description': trip.description
        },
        'entry_list': list(entry_list)
    })


@login_required
def trip_modification_description(request, tid):
    if request.method == 'POST':
        trip = get_object_or_404(Trip, tid=tid)
        if not Trip_Person.objects.filter(tid=tid, pid=request.person.pid).exists():
            return JsonResponse({
                'success': False,
                'message': '你没有权限修改此行程'
            }, status=403)
        
        trip.description = request.POST.get('description', '')
        trip.save()

        return JsonResponse({
            'success': True,
            'message': '行程描述已更新',
            'trip': {
                'tid': trip.tid,
                'description': trip.description
            }
        })

    return JsonResponse({
        'success': False,
        'message': '请求无效'
    }, status=400)


@login_required
def trip_modification_notes(request, tid):
    if request.method == 'POST':
        trip = get_object_or_404(Trip, tid=tid)
        if not Trip_Person.objects.filter(tid=tid, pid=request.person.pid).exists():
            return JsonResponse({
                'success': False,
                'message': '你没有权限修改此行程'
            }, status=403)

        tp = get_object_or_404(Trip_Person, tid=tid, pid=request.person.pid)
        tp.notes = request.POST.get('notes', '')
        tp.save()

        return JsonResponse({
            'success': True,
            'message': '备注已更新',
            'notes': tp.notes
        })

    return JsonResponse({
        'success': False,
        'message': '请求无效'
    }, status=400)
