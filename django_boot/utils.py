from .models import Dict, Config, Notification


def notify(user, title, content):
	return user.notifications.create(title=title, content=content)


def get_dict(value):
	d = Dict.objects.get(value=value)
	return d.items.all() if d else []


def get_config(name, default_value):
	c = Config.objects.get(name=name)
	return c.value if c else default_value
