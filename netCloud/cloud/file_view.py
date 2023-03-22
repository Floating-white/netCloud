import logging

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.views import APIView

from . import model_helper
from . import xdata
from .views import R
from .serializer import FileSerial
from .util_helper import HDFSHelper

logger = logging.getLogger(__name__)


@api_view(['GET'])
def query_dir_sub_files(req: Request):
    file_id = req.data.get('file_id')
    files = model_helper.FileHelper.query_dir_sub_files(file_id)

    # file_path = req.data.get('file_path')
    # path = xdata.HDFS_PATH_PREFIX + user_id + file_path


class FileList(APIView):

    @staticmethod
    def get(req: Request):
        """获取该文件夹下面的所有文件"""
        file_id = req.data.get('file_id')
        file = model_helper.FileHelper.query_by_id(file_id)
        sub_file_list = []
        if file and file.file_type == xdata.FILE_TYPE_DIRECTORY:
            sub_file_ids = file.sub_file_ids
            for fid in sub_file_ids:
                sub_file = model_helper.FileHelper.query_by_id(fid)
                sub_file_list.append(sub_file)

            file_serial = FileSerial(instance=sub_file_list, many=True)
            return R.success(file_serial.data)
        return R.error('file is not found or file type is not directory')


class File(APIView):
    @staticmethod
    def get(req: Request):
        """文件下载"""
        fid = req.data.get('file_id')
        file = model_helper.FileHelper.query_by_id(fid)
        if file:
            # HDFSHelper.getfile()
            pass