import re
import json

from django import template
from ..models import SidebarItem

register = template.Library()


@register.inclusion_tag('_layout/navbar_items.html', takes_context=True)
def navbar_items(context):
    request = context['request']

    def process_subitem(item):
        item.active = bool(item.pattern and re.match(
            item.pattern, request.path))
        return {
            'name': item.name,
            'url': item.url,
            'active': bool(item.pattern and re.match(item.pattern, request.path)),
            'permission': item.permission and f'{item.permission.content_type.app_label}.{item.permission.codename}',
        }

    def process_item(item):
        children = list(
            map(process_subitem, item.children.all().order_by('order')))
        return {
            'name': item.name,
            'url': item.url,
            'icon': item.icon,
            'active': bool(item.pattern and re.match(item.pattern, request.path)),
            'has_children': bool(children),
            'children': children,
            'expand': any(1 for i in children if i['active']),
            'permission': item.permission and f'{item.permission.content_type.app_label}.{item.permission.codename}',
        }
    # todo: https://stackoverflow.com/questions/10778988/how-do-i-delete-a-cached-template-fragment-in-django
    items = SidebarItem.objects.filter(parent=None).all().order_by('order')
    context['items'] = list(map(process_item, items))
    return context


@register.filter()
def has_perm(user, permission):
    if permission:
        return user.has_perm(permission)
    return True


@register.filter()
def has_perms(user, *permission):
    return user.has_perms(*permission)


@register.filter()
def unread_notification(user):
    return user.notifications.filter(readed=False).count()
