from django.contrib.auth import authenticate, login
from rest_framework.request import Request
from rest_framework.views import APIView

from django.db import transaction

from . import model_helper
from .serializer import UserSerial
from .views import R

from .util_helper import LogHelper, RedisHelper, HDFSHelper

logger = LogHelper.get_logger(__name__)


class UserView(APIView):

    @staticmethod
    def post(req: Request):
        """用户注册"""
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
        conn = RedisHelper.get_conn()
        validate_code_ = conn.get(to)

        logger.debug('validate_code: {}, validate_code_: {}'.format(validate_code, validate_code_))
        if str(validate_code) != str(validate_code_):  # 校验验证码
            return R.error('validate code is error')
        username = req.data.get('username')
        password = req.data.get('password')

        with transaction.atomic():
            try:
                # 创建用户
                user = model_helper.UserHelper.create(username=username, password=password, email=to)
                logger.debug('user: {}'.format(user))
                # 在hdfs上面创建用户文件夹
                path = HDFSHelper.make_hdfs_path(user.ident)
                is_successful = HDFSHelper.create_dir(path)
                if is_successful:
                    # 在数据库中保存用户文件夹信息
                    model_helper.FileHelper.create_user_dir(user.ident)
                return R.success(UserSerial(instance=user).data)
            except Exception as e:
                if is_successful:
                    HDFSHelper.remove_dir(path)
                logger.error('error: {}'.format(e))
                return R.error('create user failed')

    @staticmethod
    def delete(req: Request):
        """注销用户"""

        pass


class UserMgrView(APIView):

    @staticmethod
    def post(req: Request):
        """登录"""
        logger.info('request params: {}'.format(req.data))
        user = authenticate(req, **req.data)
        if user is None:
            return R.error('password error or username is not exit')
        logger.info('user: {} login succeed'.format(user.id))
        login(req, user)
        return R.success(UserSerial(instance=user).data)
