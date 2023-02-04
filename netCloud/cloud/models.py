import json

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# Create your models here.
class File(models.Model):
    FILE_TYPE = [('F', 'File'), ('D', 'Directory')]

    file_name = models.CharField(max_length=64, verbose_name='文件名')
    file_type = models.CharField(max_length=1, choices=FILE_TYPE, verbose_name='文件类型')
    file_size = models.IntegerField(verbose_name='文件大小(Bytes)')
    store_path = models.CharField(max_length=320, verbose_name='HDFS存储路径')

    class Meta:
        db_table = 'file'
        verbose_name = '文件'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.file_name

class User(AbstractUser):
    is_subscribe = models.BooleanField(default=False, verbose_name='是否订阅')
    disk_remaining = models.BigIntegerField(default=1024 * 1024 * 1024, verbose_name='用户存储空间剩余容量(Bytes)')
    disk_total = models.BigIntegerField(default=1024 * 1024 * 1024, verbose_name='用户存储空间总量(Bytes)')
    files = models.ManyToManyField(to=File, related_name='users', verbose_name='用户文件')
    friends = models.ManyToManyField(to='self', verbose_name='好友')

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

class SubRecord(models.Model):
    SUB_TYPE = [(1, 'month'), (3, 'months'), (6, 'half'), (12, 'year'), (-1, 'continue_sub')]
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sub_records',
                             verbose_name='用户')
    subscribe_at = models.DateTimeField(auto_now_add=True, verbose_name='订阅开始时间')
    subscribe_type = models.IntegerField(choices=SUB_TYPE, verbose_name='订阅类型')
    invalid = models.BooleanField(default=False, verbose_name='订阅是否到期')

    class Meta:
        db_table = 'sub_record'
        verbose_name = '订阅记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        _str = {
            'sub_id': self.id,
            'sub_type': self.subscribe_type,
            'invalid': self.invalid
        }
        return json.dumps(_str)

class FileOperateRecord(models.Model):
    OPERATE_TYPE = [('U', 'Upload'), ('D', 'Down'), ('S', 'Share')]

    operate_type = models.CharField(max_length=1, choices=OPERATE_TYPE, verbose_name='操作类型')
    operate_at = models.DateTimeField(auto_now_add=True, verbose_name='操作时间')

    file = models.ForeignKey(to=File, on_delete=models.CASCADE, related_name='file_operate_records', verbose_name='文件')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='file_operate_records', verbose_name='用户')

    class Meta:
        db_table = 'file_operator_record'
        verbose_name = '文件操作记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        _str = {
            'op_type': self.operate_type,
            'op_file': self.file,
            'op_user': self.user
        }
        return json.dumps(_str)