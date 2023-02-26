from django.urls import path
from .views import user_login, get_validate_code
from .subscribe_view import Subscribe, query_sub_expire_info

urlpatterns = [
    path('login', user_login),
    path('validate', get_validate_code),
    path('subscribe', Subscribe.as_view()),
    path('subscribe_expire_info', query_sub_expire_info),
]