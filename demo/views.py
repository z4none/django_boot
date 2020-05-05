from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import FormView

from django_boot.admin import admin_site as site
from .forms import UserForm, UserProfileForm, UserAvatarForm


def profile(request):
    context = site.each_context(request)
    context['user_form'] = UserForm(instance=request.user)
    context['profile_form'] = UserProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', context)


class ProfileView(View):
    def get(self, request):
        context = site.each_context(request)
        context['user_form'] = UserForm(instance=request.user)
        context['profile_form'] = UserProfileForm(instance=request.user.profile)
        context['avatar_form'] = UserAvatarForm(instance=request.user.profile)
        return render(request, 'profile.html', context)

    def post(self, request):
        save = request.POST.get('_save')
        if save == 'info':
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = UserProfileForm(request.POST, instance=request.user.profile)

            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save(commit=False)
                user.profile = profile_form.save()
                user.save()
                messages.success(request, '用户信息已保存')
        else:
            avatar_form = UserAvatarForm(request.POST, request.FILES, instance=request.user.profile)
            if avatar_form.is_valid():
                avatar_form.save()
                messages.success(request, '用户头像已保存')

        return redirect(reverse('demo:profile'))
