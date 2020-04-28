from django import template


register = template.Library()


@register.filter()
def has_perm(user, permission):
    if permission:
        return user.has_perm(permission)
    return True


@register.filter()
def has_perms(user, *permission):
    return user.has_perms(*permission)
