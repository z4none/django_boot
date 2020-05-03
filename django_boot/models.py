import datetime

from django.db import models
from django.contrib.auth.models import User, Permission
from django.db.models.signals import post_save
from django.dispatch import receiver
from fontawesome_5.fields import IconField
from mptt.models import MPTTModel, TreeForeignKey


class Foo(models.Model):
    class Meta:
        verbose_name = 'Foo'
        verbose_name_plural = 'Foos'

    def __str__(self):
        return f'foo: {self.name}'

    name = models.CharField('name', max_length=100)


class Dashboard(models.Model):
    class Meta:
        verbose_name = "控制台"
        managed = False  # wont create model table


class Profile(models.Model):
    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    user = models.OneToOneField(
        User, verbose_name='用户', on_delete=models.CASCADE, related_name='profile')

    phone = models.CharField('手机号码', max_length=20, blank=True)

    avatar = models.ImageField('头像', upload_to='avatar/%Y%m%d/', blank=True)

    bio = models.TextField('个人资料', max_length=500, blank=True)

    need_modify_password = models.BooleanField('需要修改密码', default=False)

    def __str__(self):
        return '<user profile: {}>'.format(self.user.username)

    def get_avatar_url(self, request):
        if self.avatar:
            return request.build_absolute_uri(self.avatar.url)
        return ''


# 信号接收函数，每当新建 User 实例时自动调用
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# 信号接收函数，每当更新 User 实例时自动调用
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Config(models.Model):
    name = models.CharField('名称', max_length=200, unique=True)
    value = models.TextField('值', max_length=200, blank=True)
    description = models.TextField('描述', blank=True)

    class Meta:
        verbose_name = '配置'
        verbose_name_plural = verbose_name
        indexes = [models.Index(fields=['name']), ]
        permissions = [
            ('can_set_config', '可以编辑配置的值')
        ]

    def __str__(self):
        return f'配置: {self.name}'


class Dict(models.Model):
    parent = models.ForeignKey(
        'self', verbose_name='字典', related_name='items', null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField('名称', max_length=100)
    value = models.CharField('值', max_length=100, blank=True)
    order = models.IntegerField('顺序', default=0)

    class Meta:
        verbose_name = '字典'
        verbose_name_plural = verbose_name
        indexes = [models.Index(fields=['name']), ]
        ordering = ['order', 'name']

    def __str__(self):
        return f'字典: {self.name}'


class Org(MPTTModel):
    name = models.CharField('名称', max_length=50, unique=True)
    parent = TreeForeignKey('self', verbose_name='上级组织', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')

    users = models.ManyToManyField(
        User,
        blank=True,
        related_name='orgs'
    )

    class Meta:
        verbose_name = '组织'
        verbose_name_plural = verbose_name

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return f'组织: {self.name}'


class Notification(models.Model):
    class Meta:
        verbose_name = "notification"

    title = models.CharField('title', max_length=200)
    content = models.TextField('content')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    create_tm = models.DateTimeField('created time', default=datetime.datetime.now)
    readed = models.BooleanField('readed', default=False)
    read_tm = models.DateTimeField('read time', null=True)


