import logging

from django.db import transaction
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.views import APIView

from . import model_helper, xdata
from .models import User
from .views import R
from .serializer import SubRecordSerial

logger = logging.getLogger(__name__)



class Subscribe(APIView):
    """
        查询指定用户的订阅记录
    """

    @staticmethod
    def get(req: Request):
        user_id = req.data.get('user_id')
        records = model_helper.SubRecordHelper.query_records_by_user_id(user_id)
        serial = SubRecordSerial(instance=records, many=True)
        return R.success(serial.data)

    """
        订阅
    """

    @staticmethod
    def post(req: Request):
        """
        req: {
            user_id: xxx,
            sub_type: xxx
        }
        """
        sub_type = req.data.get('sub_type')
        user_id = req.data.get('user_id')

        try:
            user = model_helper.UserHelper.by_id(user_id)
        except User.DoesNotExist:
            return R.error('user is not found')
        # 增加用户权限
        user.is_subscribe = True
        user.disk_total += 5 * xdata.GIGABYTE
        user.disk_remaining += 5 * xdata.GIGABYTE
        # 保存订阅记录
        sub_record = model_helper.SubRecordHelper.create(user, sub_type)

        with transaction.atomic():
            user.save(update_fields=['is_subscribe', 'disk_total', 'disk_remaining'])
            sub_record.save()

        return R.success('success')


"""
    查询用户订阅的过期时间
"""


@api_view(['GET'])
def query_sub_expire_info(req: Request):
    user_id = req.data.get('user_id')
    expire_info = model_helper.SubRecordHelper.query_user_sub_expire_info(user_id)
    return R.success(expire_info)
