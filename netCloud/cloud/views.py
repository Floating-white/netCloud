import logging
import random
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .util_helper import RedisHelper

logger = logging.getLogger(__name__)



class R:
    @staticmethod
    def success(data=None):
        return Response(data={
            'r': 0,
            'msg': '',
            'data': data
        })

    @staticmethod
    def error(msg=''):
        return Response(data={
            'r': 1,
            'msg': msg,
            'data': None
        })

@api_view(['GET'])
def get_validate_code(req: Request):
    """
    req: {
        email: xxxx
    }

    resp: {
        data: {
            validate_code: xxxx
        }
    }

    """
    ex_time = 60 * 5  # second
    to = req.data.get('email')
    assert to is not None
    validate_code = '%06d' % random.randint(0, 999999)

    subject = 'netCloud 注册验证码'
    message = '验证码: {}, 有效时间{}分钟'.format(validate_code, ex_time / 60)

    conn = RedisHelper.get_conn()
    conn.setex(name=to, value=validate_code, time=ex_time)  # 存储该邮箱的验证码
    r = send_mail(subject, message, from_email=settings.EMAIL_HOST_USER, recipient_list=[to])
    if r:
        return R.success({
            'validate_code': validate_code
        })
    else:
        return R.error('error')


