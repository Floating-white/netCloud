import logging

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.views import APIView

from django.db import transaction

import model_helper
from .redis_pool import get_redis_conn
from .serializer import UserSerial
from .views import R

logger = logging.getLogger(__name__)


class UserView(APIView):
    """
        用户注册
    """

    @staticmethod
    def post(req: Request):
        """
        req: {
            username: xxx,
            password: xxx,
            email: xxx,
            validate_code: xxx
        }

        resp: {
            r: 0,
            msg: '',
            data: None
        }
        """
        to = req.data.get('email')
        validate_code = req.data.get('validate_code')
        conn = get_redis_conn()
        validate_code_ = conn.get(to)

        logger.debug('validate_code: {}, validate_code_: {}'.format(validate_code, validate_code_))
        if str(validate_code) != str(validate_code_):
            return R.error('validate code is error')
        username = req.data.get('username')
        password = req.data.get('password')
        with transaction.atomic():
            user = model_helper.UserHelper.create(username=username, password=password, email=to)
            model_helper.FileHelper.create()

            if user is None:
                return R.error('create user fail')
            else:  # 用户创建成功

                return R.success(UserSerial(instance=user).data)
