from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, HttpResponse
import requests
from django.views.decorators.csrf import csrf_exempt
import simplejson as json
from .models import Contact, Userdata


""" FUNCTIONS FOR CREATE NEW AND DELETE OR UPDATE CONTACTS OF USERS """


def add(request):
    return_dict = dict()
    data = request.POST
    contact_id = data.get("id")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    country = data.get("country")
    town = data.get("town")
    phone_nmb = data.get("phone_nmb")
    email = data.get("email")

    try:
        Contact.objects.update_or_create(first_name=first_name, last_name=last_name,
                                         user_id=contact_id,
                                         defaults={'country': country, 'town': town,
                                                   'email': email, 'phone_nmb': phone_nmb})
    except ValueError:
        return_dict["description"] = "input_error"
    else:
        return_dict["description"] = "you add one row"

    return JsonResponse(return_dict)


def get_value(request):
    return_dict = dict()
    data = request.POST
    link_id = data.get("link_id")
    try:
        prov = Contact.objects.get(id=link_id)
    except ObjectDoesNotExist:
        return_dict["description"] = "Object does not exist"
    else:
        return_dict["first_name_get"] = prov.first_name
        return_dict["last_name_get"] = prov.last_name
        return_dict["country_get"] = str(prov.country)
        return_dict["town_get"] = prov.town
        return_dict["phone_nmb_get"] = prov.phone_nmb
        return_dict["email_get"] = prov.email

    return JsonResponse(return_dict)


def delete_row(request):
    return_dict = dict()
    data = request.POST
    link_id = data.get("link_id")
    try:
        Contact.objects.get(id=link_id).delete()
    except ObjectDoesNotExist:
        return_dict["description"] = "Object does not exist"

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
    try:
        prov = Contact.objects.get(id=link_id)
    except ObjectDoesNotExist:
        return_dict["description"] = "Object does not exist"
    else:
        try:
            prov.first_name = first_name
            prov.last_name = last_name
            prov.country = country
            prov.town = town
            prov.phone_nmb = phone_nmb
            prov.email = email
            prov.save()
        except ValueError:
            return_dict["description"] = "input_error"
        else:
            return_dict["description"] = "you successfully updated your contact"

    return JsonResponse(return_dict)


""" SEND CONTACTS OF USER TO GETVERO """


def send_contacts(request):
    return_dict = dict()
    data = request.POST
    status_user = data.get("status_user")
    print(status_user)
    active_user = request.user.id

    if not Userdata.objects.filter(user_id=active_user):
        return_dict["status_user_POST"] = False

    else:
        user_api_key = Userdata.objects.get(user_id=active_user).api_key
        print(user_api_key)
        for contact in Contact.objects.filter(user_id=active_user):
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
                                   birthday=None, user_id=request.user.id)

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
    user_contacts = Contact.objects.filter(user_id=request.user.id).order_by('-created')
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
            3: str(contact.country),
            4: contact.town,
            5: str(contact.phone_nmb),
            6: contact.email,
            7: str(contact.birthday),
            8: contact.created.strftime('%m/%d/%y') if contact.created else '',
        })
    return HttpResponse(json.dumps(ajax_response), content_type='application/json')
