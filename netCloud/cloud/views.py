import logging

# Create your views here.
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['POST'])
def login(req: Request):
    """
    req: {
        username: xxx,
        password: xxx
    }

    resp: {
        r: 0,
        msg: ''
    }
    """
    username = req.data.get('username')
    password = req.data.get('password')

    logging.debug('xxxx')

    resp = {
        'r': 0,
        'msg': '',
        'data': None
    }

    return Response('')
