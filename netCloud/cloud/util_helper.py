import logging

import requests
from pyhdfs import HdfsClient
import redis

from . import xdata


class LogHelper:
    _level = logging.DEBUG
    _format = "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(lineno)s - %(message)s"
    _log_file = r"./cloud.log"
    _mode = 'w'
    logging.basicConfig(level=_level, format=_format, filename=_log_file, filemode=_mode)

    @classmethod
    def get_logger(cls, name):
        return logging.getLogger(name)


logger = LogHelper.get_logger(__name__)


class HDFSHelper:
    _hosts = ['192.168.100.3:9870']
    _user_name = 'root'

    _client = HdfsClient(hosts=_hosts, user_name=_user_name)  # type: HdfsClient

    _file_op_base_url = 'http://master:9864/webhdfs/v1'

    _download_param = {
        'op': 'OPEN',
        'user.name': 'root',
        'namenoderpcaddress': 'master:9000',
        'offset': 0
    }

    _upload_param = {
        'op': 'CREATE',
        'namenoderpcaddress': 'master:9000',
        'createflag': '',
        'overwrite': 'false'
    }

    _upload_headers = {
        'Content-Type': 'application/octet-stream'
    }

    @classmethod
    def client(cls):
        """返回HDFS客户端"""
        return cls._client

    @classmethod
    def create_dir(cls, path):
        """在HDFS上创建文件夹"""
        if not cls._client.exists(path):
            logger.debug('create user root directory: {}'.format(path))
            return cls._client.mkdirs(path, permission=777)
        logger.warning('user root directory is existed: {}'.format(path))

    @classmethod
    def remove_dir(cls, path):
        """在HDFS上删除文件夹"""
        if cls._client.exists(path):
            return cls._client.delete(path=path, recursive=True)

    @classmethod
    def remove_file(cls, path):
        """在HDFS上删除文件"""
        if cls._client.exists(path):
            return cls._client.delete(path=path)

    @staticmethod
    def make_hdfs_path(path: str):
        return xdata.HDFS_PATH_PREFIX + path

    @classmethod
    def download(cls, src, localdest):
        """下载文件"""
        url = cls._file_op_base_url + src
        resp = requests.get(url=url, params=cls._download_param)
        if resp.ok:
            logger.info('{} 下载成功'.format(src))
            data = resp.content.decode('utf-8')

            with open(localdest, 'w') as f:
                f.write(data)

            return True
        logger.error('{} 下载失败'.format(src))
        return False

    @classmethod
    def upload(cls, localsrc, dest):
        """上传文件"""
        url = cls._file_op_base_url + dest
        with open(localsrc) as f:
            resp = requests.put(url=url, params=cls._upload_param, data=f.read(), headers=cls._upload_headers)
        if resp.ok:
            logger.info('{} 上传成功'.format(localsrc))
        else:
            logger.error('{} 上传失败'.format(localsrc))


class RedisHelper:
    _host = '192.168.100.3'
    _port = 6379
    _password = 'passwd'
    _max_connections = 10

    _Pool = redis.ConnectionPool(host=_host, port=_port, password=_password, max_connections=_max_connections,
                                 decode_responses=True)

    @classmethod
    def get_conn(cls):
        if cls._Pool:
            return redis.Redis(connection_pool=cls._Pool)
        else:
            raise Exception('pool is none')
