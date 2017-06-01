from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', home),
    url(r'^register/', register),
    url(r'^add/$', add, name='add'),
    url(r'^update/$', update, name='update'),
    url(r'^user_setting/$', settings_user, name='settings_user'),
    url(r'^data_import/$', data_import, name='data_import'),
    url(r'^update/get_value/$', get_value, name='get_value'),
    url(r'^update/delete_row/$', delete_row, name='delete_row'),
    url(r'^send_contacts/$', send_contacts, name='send_contacts'),
    url(r'^list_of_contacts/$', ajax_list_of_contacts, name='list_of_contacts'),
]
