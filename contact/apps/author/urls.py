from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^$', home),
    url(r'^register/', Register.as_view(), name='register'),
    url(r'^user_setting/$', Settings.as_view(), name='settings_user'),
]
