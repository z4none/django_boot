from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render


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
        # request.current_app = self.name
        return render(request, "test.html", self.each_context(request))

    def home(self, request):
        # request.current_app = self.name
        return render(request, "home.html", self.each_context(request))

    def get_urls(self):
        from django.conf.urls import url
        urls = super(AdminSite, self).get_urls()
        urls += [
            url(r'^home/$', self.admin_view(self.home)),
            url(r'^test/$', self.admin_view(self.test))
        ]
        return urls
