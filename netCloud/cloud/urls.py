from django.urls import path
from .views import get_validate_code
from .subscribe_view import Subscribe, query_sub_expire_info
from .user_view import UserView, UserMgrView
from .file_view import FileList

urlpatterns = [
    path('validate', get_validate_code),
    path('sub', Subscribe.as_view()),
    path('sub_info', query_sub_expire_info),
    path('usermgr', UserMgrView.as_view()),
    path('user', UserView.as_view()),
    path('filelist', FileList.as_view()),

]
