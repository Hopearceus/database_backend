from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import Person
from ..album.models import Album
from django.utils import timezone


def register_view(request):
    if request.method == 'POST':
        pid = request.POST.get('pid', '')
        default_aid = request.POST.get('default_aid', '')
        if not pid or not default_aid:
            return JsonResponse({'success': False, 'message': '缺少 pid 或 default_aid 参数'}, status=400)

        form = CustomUserCreationForm(request.POST)

        album = Album(pid=pid, aid=default_aid, description='默认相册', time=timezone.now())
        album.save()

        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({'success': True, 'message': '注册成功，已自动登录', 'redirect_url': 'login'})
        else:
            return JsonResponse({'success': False, 'message': '表单数据无效', 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'success': False, 'message': '请求方法不允许'}, status=405)

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            password = form.cleaned_data.get('password')
            person = authenticate(name=name, password=password)
            if person is not None:
                login(request, person)
                next_url = request.GET.get('next', 'home')
                return JsonResponse({'success': True, 'message': '登录成功', 'redirect_url': next_url})
            else:
                return JsonResponse({'success': False, 'message': '用户名或密码错误'}, status=400)
        else:
            return JsonResponse({'success': False, 'message': '表单数据无效', 'errors': form.errors}, status=400)
    else:
        return JsonResponse({'success': False, 'message': '请求方法不允许'}, status=405)

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Person
    form_class = UserProfileForm
    template_name = 'person/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.person

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.is_ajax():
            return JsonResponse({'success': True})
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.is_ajax():
            return JsonResponse({'success': False, 'errors': form.errors})
        return response