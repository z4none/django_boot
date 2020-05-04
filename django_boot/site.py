from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .utils import get_dict, notify


class AdminSite(admin.AdminSite):
    site_header = 'my site header'

    def get_context(self, request):
        app_list = self.get_app_list(request)

        context = {
            **self.each_context(request),
            'title': self.index_title,
            'app_list': self.get_app_list(request),
        }

        return context

    def test(self, request):
        context = self.each_context(request)
        context['items'] = get_dict('android_mobile_mfr')
        return render(request, "test.html", context)

    def test_notification(self, request):
        notify(request.user, 'test notification', f'this is a test notification')
        return redirect("/test")

    def notification_detail(self, request, id):
        obj = get_object_or_404(request.user.notifications, pk=id)
        context = self.each_context(request)
        context['obj'] = obj
        context['title'] = obj.title
        return render(request, "dbt/notification/detail.html", context)

    def notification_mark_as_readed(self, request, id):
        obj = get_object_or_404(request.user.notifications, pk=id)
        obj.readed = True
        obj.save()
        url = reverse('admin:notification-detail', args=(obj.id,))
        return redirect(url)

    def home(self, request):
        # request.current_app = self.name
        return render(request, "home.html", self.each_context(request))

    def get_urls(self):
        from django.urls import path
        from django.conf.urls import url
        urls = super(AdminSite, self).get_urls()
        urls += [
            url(r'^home/$', self.admin_view(self.home)),
            url(r'^test/$', self.admin_view(self.test)),
            url(r'^test-notification/$', self.admin_view(self.test_notification)),
            path('dbt/notification/<id>/detail', self.admin_view(self.notification_detail), name='notification-detail'),
            path('dbt/notification/<id>/mark-as-readed', self.admin_view(self.notification_mark_as_readed), name='notification-mark-as-readed'),
        ]
        return urls
