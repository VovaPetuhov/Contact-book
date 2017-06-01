from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.views.decorators.csrf import csrf_exempt

from .forms import UserRegistrationForm, UserSettingForm_pas, UserSettingForm_api
from .models import Contact, Userdata
from django.http import JsonResponse
import simplejson as json
import requests


def home(request):
    all_contacts = Contact.objects.all()

    return render(request, 'book_of_contacts/home.html', locals())


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

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

    else:
        form = UserRegistrationForm()

    return render(request, 'book_of_contacts/register.html', {'form': form})


""" USER SETTINGS """


def settings_user(request):
    if request.method == 'POST':
        form_sett_pas = UserSettingForm_pas(request.POST)
        form_sett_api = UserSettingForm_api(request.POST)
        active_user = request.user.id

        if form_sett_pas.is_valid():
            user_change = form_sett_pas.cleaned_data
            password = user_change['password']
            select_user = User.objects.get(id=active_user)
            select_user.set_password(password)
            select_user.save()

            return HttpResponseRedirect('/')

        elif form_sett_api.is_valid():
            api_change = form_sett_api.cleaned_data
            api_key = str(api_change['api_key'])

            if not Userdata.objects.filter(username_id=active_user):
                select_api = Userdata.objects.create(api_key=api_key, username_id=active_user)
            else:
                select_api = Userdata.objects.get(username_id=active_user)
                select_api.api_key = api_key
            select_api.save()

            return HttpResponseRedirect('/')

    else:
        form_sett_pas = UserSettingForm_pas()
        form_sett_api = UserSettingForm_api()

    return render(request, 'book_of_contacts/user_setting.html', {'form_sett_pas': form_sett_pas,
                                                                  'form_sett_api': form_sett_api})


""" FUNCTIONS FOR CREATE NEW AND DELETE OR UPDATE CONTACTS OF USERS """


def add(request):
    return_dict = dict()
    # key = request.session.session_key
    data = request.POST
    contact_id = data.get("id")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    country = data.get("country")
    town = data.get("town")
    phone_nmb = data.get("phone_nmb")
    email = data.get("email")

    new_contact, created = Contact.objects.update_or_create(first_name=first_name, last_name=last_name,
                                                            username_id=contact_id,
                                                            defaults={'country': country, 'town': town,
                                                                      'email': email, 'phone_nmb': phone_nmb})

    if created:
        user_id = new_contact.id
        return_dict["user_id"] = user_id
        return_dict["created"] = created

    print(created)

    return JsonResponse(return_dict)


def get_value(request):
    return_dict = dict()
    data = request.POST
    link_id = data.get("link_id")
    prov = Contact.objects.get(id=link_id)
    return_dict["first_name_get"] = prov.first_name
    return_dict["last_name_get"] = prov.last_name
    return_dict["country_get"] = prov.country
    return_dict["town_get"] = prov.town
    return_dict["phone_nmb_get"] = prov.phone_nmb
    return_dict["email_get"] = prov.email

    return JsonResponse(return_dict)


def delete_row(request):
    return_dict = dict()
    data = request.POST
    link_id = data.get("link_id")
    print(link_id)
    Contact.objects.get(id=link_id).delete()

    return JsonResponse(return_dict)


def update(request):
    return_dict = dict()
    data = request.POST
    link_id = data.get("link_id")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    country = data.get("country")
    town = data.get("town")
    phone_nmb = data.get("phone_nmb")
    email = data.get("email")

    print(first_name)
    print(link_id)
    prov = Contact.objects.get(id=link_id)
    prov.first_name = first_name
    prov.last_name = last_name
    prov.country = country
    prov.town = town
    prov.phone_nmb = phone_nmb
    prov.email = email
    prov.save()

    return JsonResponse(return_dict)


""" SEND CONTACTS OF USER TO GETVERO """


def send_contacts(request):
    return_dict = dict()
    data = request.POST
    status_user = data.get("status_user")
    print(status_user)
    active_user = request.user.id

    if not Userdata.objects.filter(username_id=active_user):
        return_dict["status_user_POST"] = False

    else:
        user_api_key = Userdata.objects.get(username_id=active_user).api_key
        print(user_api_key)
        for contact in Contact.objects.filter(username_id=active_user):
            requests.request('POST', 'https://api.getvero.com/api/v2/users/track',
                             json={'auth_token': user_api_key, 'id': contact.id, 'email': contact.email,
                                   'data': {'first_name': contact.first_name,
                                            'last_name': contact.last_name,
                                            'country': contact.country,
                                            'town': contact.town
                                            }
                                   })

    return JsonResponse(return_dict)


""" IMPORT DATA FROM CSV-files"""


@csrf_exempt
def data_import(request):
    if request.method == 'POST':

        csv_file = request.FILES['data_input_file']
        fs = FileSystemStorage()
        fs.save('temp_import.csv', csv_file)
        csv_data =fs.open('temp_import.csv', mode='r')
        count = -1

        for row in csv_data:
            count = count + 1
            row = row.split(',')
            if row[0] == 'number':
                continue

            Contact.objects.create(session_key=None, first_name=row[1], last_name=row[2], country=row[3],
                                   town=row[4], phone_nmb=int(row[5]), email=row[6],
                                   birthday=None, username_id=request.user.id)

        fs.delete('temp_import.csv')
        print('count: '+str(count))
        return HttpResponse(json.dumps({'count': count}))
    else:
        return HttpResponse(json.dumps({'error': 'Something wrong'}))


""" POST-PROCESSING FOR DATA_TABLE """


def ajax_list_of_contacts(request):

    ajax_response = {'sEcho': '', 'aaData': [], 'iTotalRecords': 0, 'iTotalDisplayRecords': 0}
    start_pos = int(request.GET['iDisplayStart'])
    end_pos = start_pos + int(request.GET['iDisplayLength'])

    # --- View contacts of login user ---
    user_contacts = Contact.objects.filter(username_id=request.user.id).order_by('-created')
    # user_contacts = Contact.objects.filter(username_id=request.user.id)

    # --- Views counts ---
    user_contacts_count = user_contacts.count()
    contacts = user_contacts[start_pos:end_pos]
    ajax_response['iTotalRecords'] = ajax_response['iTotalDisplayRecords'] = user_contacts_count

    # --- Getting data from base for send to front-end ---
    for contact in contacts:
        ajax_response['aaData'].append({
            'DT_RowId': str(contact.id),
            0: str(contact.id),
            1: contact.first_name,
            2: contact.last_name,
            3: contact.country,
            4: contact.town,
            5: str(contact.phone_nmb),
            6: contact.email,
            7: str(contact.birthday),
            8: contact.created.strftime('%m/%d/%y') if contact.created else '',
        })
    return HttpResponse(json.dumps(ajax_response), content_type='application/json')
