import logging

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.views import APIView

import model_helper
logger = logging.getLogger(__name__)


@api_view(['GET'])
def query_dir_sub_files(req: Request):
    file_id = req.data.get('file_id')
    files = model_helper.FileHelper.query_dir_sub_files(file_id)



    # file_path = req.data.get('file_path')
    # path = xdata.HDFS_PATH_PREFIX + user_id + file_path




class FileList(APIView):
    """

    """

    @staticmethod
    def get(req: Request):
        file_id = req.data.get('file_id')
