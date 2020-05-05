from django.core.exceptions import ObjectDoesNotExist

from .models import Dict, Config, Notification


def notify(user, title, content):
	return user.notifications.create(title=title, content=content)


def get_dict(value):
	try:
		return Dict.objects.get(value=value).items.all()
	except Dict.DoesNotExist:
		return []


def get_config(name, default_value):
	c = Config.objects.get(name=name)
	return c.value if c else default_value
