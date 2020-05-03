import re
import json
from django.conf import settings

from django import template

register = template.Library()


@register.inclusion_tag('_tags/navbar_menu.html', takes_context=True)
def navbar_menu(context):
    request = context['request']

    def process_sub_item(item):
        highlight = item.get('highlight')
        return {
            'name': item.get('name'),
            'url': item.get('url'),
            'active': bool(highlight and re.match(highlight, request.path)),
            'permission': item.get('permission'),
        }

    def process_item(item):
        children = list(map(process_sub_item, item.get('children', [])))
        highlight = item.get('highlight')
        return {
            'name': item.get('name'),
            'url': item.get('url'),
            'icon': item.get('icon'),
            'active': bool(highlight and re.match(highlight, request.path)),
            'has_children': bool(children),
            'children': children,
            'expand': any(1 for i in children if i['active']),
            'permission': item.get('permission'),
        }
    # todo: https://stackoverflow.com/questions/10778988/how-do-i-delete-a-cached-template-fragment-in-django
    items = settings.DB_NAVBAR_MENU
    context['navbar_menu'] = list(map(process_item, items))
    return context


@register.inclusion_tag('_tags/user_menu.html', takes_context=True)
def user_menu(context):
    context['user_menu'] = map(lambda i: {
        'name': i.get('name'),
        'url': i.get('url'),
        'is_divider': i.get('name').startswith('---')
    }, settings.DB_USER_MENU)
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
