from django.db import models
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group, Permission
from django.forms import ModelForm, TextInput
from django.urls import reverse
from django.utils.html import format_html, mark_safe
from django.core.paginator import Paginator
from django.template.response import TemplateResponse
from django.core.exceptions import PermissionDenied
from django_select2 import forms as s2forms
from mptt.admin import DraggableMPTTAdmin
from .models import Foo, Profile, Config, Dict, Org, Notification
from .site import AdminSite


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'UserProfile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


class PermissionAdmin(admin.ModelAdmin):
    search_fields = ['name']

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'object_repr',
                    'action_flag', 'action')
    list_per_page = 20
    list_display_links = None

    search_fields = ['=user__username', 'object_repr']
    fieldsets = [(None, {'fields': ()}), ]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def action(self, obj):
        return mark_safe(f'<a href="#" class="float-right">detail {obj.id}</a>')

    action.short_description = mark_safe('<span class="float-right">操作</span>')


class ConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'description')
    list_editable = ('value', )
    search_fields = ['name']
    ordering = ('name',)

    formfield_overrides = {
        models.TextField: {'widget': TextInput},
    }


class DictForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(DictForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Dict.objects.filter(parent=None)


class DictAdmin(admin.ModelAdmin):
    list_per_page = 20
    change_list_template = 'dbt/dict/change_list.html'
    form = DictForm

    def changelist_view(self, request, extra_context=None):
        if not self.has_view_or_change_permission(request):
            raise PermissionDenied

        opts = self.model._meta
        qs = self.get_queryset(request)
        p = request.GET.get('p')
        q = request.GET.get('q')
        dt = request.GET.get('dt')

        dict_qs = qs.filter(parent=None)
        if q:
            dict_qs = dict_qs.filter(name__contain=q)
        paginator = Paginator(dict_qs, self.list_per_page)
        dict_list = paginator.get_page(p)

        if dt:
            dt, item_list = int(dt), qs.filter(parent=dt)
            dict_obj = qs.get(pk=dt)
        else:
            item_list = dict_obj = None

        context = {
            **self.admin_site.each_context(request),
            'title': f'选择 字典 来修改',
            'opts': opts,
            'dt': dt,
            'dict_list': dict_list,
            'item_list': item_list,
            'dict_obj': dict_obj,
            'has_add_permission': self.has_add_permission(request),
            ** (extra_context or {}),
        }

        return TemplateResponse(request, self.change_list_template, context)


class OrgAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'row_actions')
    # list_display_links = None
    change_list_template = 'dbt/org/change_list.html'

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def row_actions(self, obj):
        url = reverse('admin:db_org_change', args=(obj.id,))
        return mark_safe(f'<a href="{url}" class="float-right">编辑</a>')

    # tree_actions.short_description = ''
    row_actions.short_description = mark_safe('<span class="float-right">操作</span>')

    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        org = request.GET.get('org')
        if org:
            request.GET.pop('org')
            org, org_obj = int(org), Org.objects.get(pk=org)
            orgs = Org.objects.prefetch_related('users').filter(
                lft__gte=org_obj.lft).filter(rght__lte=org_obj.rght)
            user_ids = set()
            for o in orgs:
                for u in o.users.all():
                    user_ids.add(u.id)
            users = User.objects.prefetch_related(
                'orgs').filter(id__in=user_ids).order_by('id')
            users = map(lambda u: {
                'username': u.username,
                'first_name': u.first_name,
                'orgs': ', '.join([o.name for o in u.orgs.all()])
            }, users)
        else:
            org = org_obj = users = None
        extra_context = extra_context or {}
        extra_context['org'] = org
        extra_context['org_obj'] = org_obj
        extra_context['users'] = users
        return super(OrgAdmin, self).changelist_view(request, extra_context=extra_context)


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('notification_title', 'create_tm', 'readed')
    list_display_links = None
    list_filter = ('readed',)
    exclude = ('user', 'create_tm', 'readed', 'read_tm')
    actions = ('make_readed', )

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'view notifications'
        return super(NotificationAdmin, self).changelist_view(request, extra_context=extra_context)

    def has_add_permission(self, request):
        return False

    def make_readed(self, request, queryset):
        rows_updated = queryset.update(readed=True)
        if rows_updated == 1:
            message_bit = "1 notification was"
        else:
            message_bit = "%s notifications were" % rows_updated
        self.message_user(request, "%s successfully marked as readed." % message_bit)

    make_readed.short_description = "Mark selected notification as readed"

    def notification_title(self, obj):
        url = reverse('admin:notification-detail', args=(obj.id,))
        return mark_safe(f'<a href="{url}">{obj.title}</a>')

    # tree_actions.short_description = ''
    notification_title.short_description = mark_safe('<span>title</span>')


admin_site = AdminSite(name='django_boot')

admin_site.register(Foo)
admin_site.register(User, UserAdmin)
admin_site.register(Group)
admin_site.register(Permission, PermissionAdmin)
admin_site.register(LogEntry, LogEntryAdmin)
admin_site.register(Config, ConfigAdmin)
admin_site.register(Dict, DictAdmin)
admin_site.register(Org, OrgAdmin)
admin_site.register(Notification, NotificationAdmin)
