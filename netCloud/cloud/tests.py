from django.test import TestCase

# Create your tests here.
from .models import SubRecord
from .model_helper import SubRecordHelper, UserHelper

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