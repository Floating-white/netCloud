import logging

from . import xdata
from .models import User, SubRecord, File
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class UserHelper:
    @staticmethod
    def create(username, password, email):
        return User.objects.create_user(username=username, password=password, email=email)

    @staticmethod
    def by_id(id):
        return User.objects.get(pk=id)


class SubRecordHelper:
    @staticmethod
    def create(user, sub_type):
        return SubRecord.objects.create(user=user, subscribe_type=sub_type)

    @staticmethod
    def query_user_sub_expire_info(user_id):
        records = SubRecord.objects.filter(user_id=user_id, invalid=False).order_by('subscribe_at')
        if not records:  # 没有有效的订阅记录
            return None
        early_valid_record = records.first()  # 最早的有效订阅记录
        invalid_days = datetime.now(tz=xdata.TIMEZONE_UTC_8) - early_valid_record.subscribe_at_utc8
        valid_days = timedelta(days=0)  # 订阅有效天数
        for _ in records:
            valid_days += timedelta(days=_.subscribe_type)
        valid_days -= invalid_days

        return {
            'valid_days': valid_days.days,
            'expire_time': datetime.now(tz=xdata.TIMEZONE_UTC_8) + valid_days
        }

    @staticmethod
    def query_records_by_user_id(user_id):
        records = SubRecord.objects.filter(user_id=user_id).order_by('subscribe_at')
        return records

    @staticmethod
    def query_user_last_record(user_id):
        last_record = SubRecord.objects.filter(user_id=user_id).order_by('-subscribe_at').first()
        return last_record


class FileHelper:
    @staticmethod
    def query_dir_sub_files(file_id):
        try:
            file = File.objects.get(pk=file_id)

        except File.DoesNotExist:
            return None
        return file

    @staticmethod
    def create_user_dir(user_id):
        path = xdata.HDFS_PATH_PREFIX + user_id

        File.objects.create(file_name=user_id, file_type=xdata.FILE_TYPE_DIRECTORY, file_size=0, store_path='')


class HDFSHelper:
    @staticmethod
    def create_dir(path):


        pass


