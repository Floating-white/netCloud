import json
import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from . import xdata


class File(models.Model):
    file_name = models.CharField(max_length=64, verbose_name='文件名')
    file_type = models.CharField(max_length=1, choices=xdata.FILE_TYPE_CHOICE, verbose_name='文件类型')
    file_size = models.FloatField(verbose_name='文件大小(KiloBytes)')
    store_path = models.CharField(max_length=320, verbose_name='HDFS存储路径')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    ext_info = models.CharField(max_length=3200, default='{}', verbose_name='扩展信息')

    class Meta:
        db_table = 'file'
        verbose_name = '文件'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.file_name

    def load_from_ext(self, key, default):
        ext = json.loads(self.ext_info)
        try:
            return ext[key]
        except KeyError:
            return default

    @property
    def sub_file_ids(self):
        return self.load_from_ext(xdata.EXT_SUB_FILE_IDS, [])


class User(AbstractUser):
    is_subscribe = models.BooleanField(default=False, verbose_name='是否订阅')
    disk_remaining = models.FloatField(default=xdata.GIGABYTE, verbose_name='用户存储空间剩余容量(KiloBytes)')
    disk_total = models.BigIntegerField(default=xdata.GIGABYTE, verbose_name='用户存储空间总量(KiloBytes)')
    files = models.ManyToManyField(to=File, related_name='users', verbose_name='用户文件')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')
    ident = models.UUIDField(default=uuid.uuid4().hex, verbose_name='标识符')
    ext_info = models.CharField(max_length=3200, verbose_name='扩展信息')

    class Meta:
        db_table = 'user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        clsname = self.__class__.__name__
        return '{}:{{' \
               'id={},' \
               'username={}, ' \
               'is_subscribe={}, ' \
               'disk_remaining={}, ' \
               'disk_total={}' \
               '}}'.format(clsname, self.id, self.username, self.is_subscribe, self.disk_remaining, self.disk_total)

    __repr__ = __str__


class SubRecord(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sub_records',
                             verbose_name='用户')
    subscribe_at = models.DateTimeField(auto_now_add=True, verbose_name='订阅开始时间')
    subscribe_type = models.IntegerField(choices=xdata.SUBSCRIBE_TYPE_CHOICE, verbose_name='订阅类型')
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

    @property
    def subscribe_at_utc8(self):
        return self.subscribe_at.astimezone(tz=xdata.TIMEZONE_UTC_8)


class FileOperateRecord(models.Model):
    operate_type = models.CharField(max_length=1, choices=xdata.OPERATE_FILE_TYPE_CHOICE, verbose_name='操作类型')
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
