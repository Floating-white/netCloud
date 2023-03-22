import os

from django.test import TestCase

# Create your tests here.
from . import xdata
from .models import SubRecord
from .model_helper import SubRecordHelper, UserHelper
from .util_helper import HDFSHelper


class Test(TestCase):

    def test_time_type(self):
        user = UserHelper.create('test', 'f', '')
        user.save()
        user = UserHelper.by_id(1)
        sub_record = SubRecordHelper.create(user, 1)
        sub_record.save()
        sub_records = SubRecord.objects.all().first()
        print(sub_records.subscribe_at)
        print(type(sub_records.subscribe_at))

    def test_hdfs_file_op(self):
        HDFSHelper.upload(os.path.join(xdata.TEMP_FILE_PATH, 'a.txt'), '/')

