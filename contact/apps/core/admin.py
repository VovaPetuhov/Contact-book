from django.contrib import admin
from .models import *


class ContactsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Contact._meta.fields]

    class Meta:
        model = Contact

admin.site.register(Contact, ContactsAdmin)


class UserDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Userdata._meta.fields]

    class Meta:
        model = Userdata

admin.site.register(Userdata, UserDataAdmin)
