from django.urls import path

from . import views
from django_boot.admin import admin_site

app_name = 'demo'
urlpatterns = [
    path('profile/', admin_site.admin_view(views.ProfileView.as_view()), name='profile'),
]
