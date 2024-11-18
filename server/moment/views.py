import os
import json

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponseForbidden

from .models import Moment, Moment_Person
from .forms import MomentForm
from ..person.models import Person
from ..album.models import Album
from ..picture.models import Picture, Picture_Moment
from ..trip.models import Trip, Trip_Person
from django.contrib.auth.decorators import login_required
from sensitive_word_filter import DFAFilter
from django.utils import timezone


@login_required
def moment_creation(request, tid):
    if request.method == 'POST':
        form = MomentForm(request.POST, request.FILES)
        if form.is_valid():
            moment = form.save(commit=False)
            moment.creator = request.person.pid
            moment.tid = None
            moment_person = Moment_Person(pid=request.user.id, mid=moment.mid)
            moment_person.save()
            if tid != None:
                moment.tid = tid
            
            dfa_filter = DFAFilter()
            filtered_text, has_sensitive_word = dfa_filter(moment.text)
            if has_sensitive_word:
                return render(request, 'moment/creation', {
                    'form': form,
                    'message': "存在敏感词，请重试！"
                })
            moment.text = filtered_text
            moment.save()
            return redirect('moment_detail', mid=moment.mid)
    else:
        form = MomentForm()
        return render(request, 'moment/creation.html', {
            'form': form
        })

@login_required
def moment_deletion(request, mid):
    moment = get_object_or_404(Moment, mid=mid, creator=request.user.person)
    if request.method == 'POST':
        if moment.creator == request.user:
            moment.delete()
            #TODO: also check
            return JsonResponse({'success': True, 'message': '圈子已删除'})
        else:
            return JsonResponse({'success': False, 'message': '你没有权限删除此圈子'})
    return JsonResponse({'success': False, 'message': '请求无效'})

@login_required
def moment_detail(request, mid):
    moment = get_object_or_404(Moment, mid=mid)
    trip = get_object_or_404(Trip, tid=moment.tid)
    pid_set = list(Picture_Moment.objects.filter(mid=mid).values_list('pid', flat=True).distinct())
    pic_list = Picture.objects.filter(pid__in=pid_set)
    return render(request, 'moment/detail.html', {
        'moment': moment,
        'trip': trip,
        'pic_list': pic_list
    })

@login_required
def trip_share(request, tid):
    return moment_creation(request, tid)

@login_required
def moment_comment(request, mid):
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        moment = get_object_or_404(Moment, mid=mid)
        try:
            moment_person = Moment_Person.objects.filter(pid=request.person.pid, mid=moment.mid)
            moment_person.text = comment_text
            moment_person.like = request.POST.get('like')
            moment_person.time = timezone.now()
            moment_person.save()
        except Moment_Person.DoesNotExist:
            moment_person = Moment_Person(pid=request.user.id, mid=moment.mid, text=comment_text, like=None, time=timezone.now())
            moment_person.save()
        return redirect('moment_detail', mid=mid)
    moment = get_object_or_404(Moment, mid=mid)
    return render(request, 'moment/comment.html', {'moment': moment})

@login_required
def moment_add_picture(request, mid, pid):
    pm = Picture_Moment(mid=mid, pid=pid)
    return redirect('moment_detail', mid=mid)