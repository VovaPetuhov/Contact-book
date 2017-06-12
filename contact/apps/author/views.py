from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from .forms import *
from django.contrib.auth.models import User
from ..core.models import Userdata


def home(request):
    return render(request, 'home.html', locals())


class Register(View):
    form_class = UserRegistrationForm
    initial = {'key': 'value'}
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user_obj = form.cleaned_data
            username = user_obj['username']
            email = user_obj['email']
            password = user_obj['password']
            if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
                User.objects.create_user(username, email, password)
                user = authenticate(username=username, password=password)
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                raise forms.ValidationError('Looks like a username with that email or password already exists')


class Settings(View):
    form_sett_pas = UserSettingForm_pas
    form_sett_api = UserSettingForm_api
    initial = {'key': 'value'}
    template_name = 'user_setting.html'

    def get(self, request, *args, **kwargs):
        form_pass = self.form_sett_pas(initial=self.initial)
        form_api = self.form_sett_api(initial=self.initial)
        return render(request, self.template_name, {'form_sett_pas': form_pass,
                                                    'form_sett_api': form_api})

    def post(self, request, *args, **kwargs):
        active_user = request.user.id
        form_pass = self.form_sett_pas(request.POST)
        form_api = self.form_sett_api(request.POST)

        if form_pass.is_valid():
            user_change = form_pass.cleaned_data
            password = user_change['password']
            select_user = User.objects.get(id=active_user)
            select_user.set_password(password)
            select_user.save()

        elif form_api.is_valid():
            api_change = form_api.cleaned_data
            api_key = str(api_change['api_key'])
            if not Userdata.objects.filter(user_id=active_user):
                select_api = Userdata.objects.create(api_key=api_key, user_id=active_user)
            else:
                select_api = Userdata.objects.get(username_id=active_user)
                select_api.api_key = api_key
            select_api.save()

        return HttpResponseRedirect('/')
