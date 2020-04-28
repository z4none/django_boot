from .models import Notification


def notify(user, title, content):
	return user.notifications.create(title=title, content=content)
