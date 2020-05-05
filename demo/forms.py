
from django.contrib.auth.models import User


from django_boot.models import Profile
from django_boot.widgets import ImageWidget
from django.forms import ModelForm


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email']


class UserProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'bio']


class UserAvatarForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': ImageWidget(),
        }
