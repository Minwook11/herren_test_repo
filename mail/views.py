import json
import re
import requests

from django.views import View
from django.http  import JsonResponse
from django.db    import IntegrityError

from .models import Address

def send_mail(address, subject, content):
    url = 'http://python.recruit.herrencorp.com/api/v1/mail'
    headers = {
        'Content-Type'  : 'application/x-www-form-urlencoded',
        'Authorization' : 'herren-recruit-python'
    }
    data = {
        'mailto'  : address,
        'subject' : subject,
        'content' : content
    }
    response = requests.post(url = url, data = data, headers = headers)

    return response.json()['status']

class SubscribeView(View):
    def post(self, request):
        try:
            data        = json.loads(request.body)
            input_name  = data['name']
            input_email = data['email']

            is_email_form = re.compile('[@]((\.)|(([\w-]+\.)+))')
            if not(is_email_form.search(input_email)):
                return JsonResponse({'message' : 'WRONG_EMAIL_FORMAT'}, status = 400)

            Address(
                name  = input_name,
                email = input_email
            ).save()
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

        except IntegrityError:
            return JsonResponse({'message' : 'DUPLICATE_EMAIL'}, status = 400)

        return JsonResponse({'message' : 'REGIST_SUCCESS'}, status = 200)

class UnsubscribeView(View):
    def delete(self, request):
        try:
            data        = json.loads(request.body)
            input_email = data['email']

            is_email_form = re.compile('[@]((\.)|(([\w-]+\.)+))')
            if not(is_email_form.search(input_email)):
                return JsonResponse({'message' : 'WRONG_EMAIL_FORMAT'}, status = 400)

            if not(Address.objects.filter(email = input_email).exists()):
                return JsonResponse({'message' : 'WRONG_EMAIL_USED'}, status = 400)

            target = Address.objects.get(email = input_email)
            target.delete()
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)

        return JsonResponse({'message' : 'DELETE_SUCCESS'}, status = 200)

class SendView(View):
    def get(self, request, *args, **kwargs):
        target = request.GET.get('target', None)
        subject = 'Mail send TEST'
        content = 'THIS IS JUST TEST'
        if not(target):
            address_list = Address.objects.all()
            if not(address_list):
                return JsonResponse({'message' : 'EMPTY_EMAIL_LIST'}, status = 400)

            all_response = [{
                'name'    : address.name,
                'email'   : address.email,
                'subject' : subject,
                'content' : content,
                'result'  : send_mail(address.email, subject, content)
            } for address in address_list]

            return JsonResponse({'message' : all_response}, status = 200)

        if target:
            address = Address.objects.get(email = target)
            if not(address):
                return JsonResponse({'message' : 'WRONG_TARGET_EMAIL'}, status = 400)

            response = {
                'name'    : address.name,
                'subject' : subject,
                'content' : content,
                'result'  : send_mail(address.email, subject, content)
            }

            return JsonResponse({'message' : response}, status = 200)

class ListView(View):
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email', None)
        if not(email):
            return JsonResponse({'message' : 'WRONG_EMAIL_ADDRESS'}, status = 400)

        url = 'http://python.recruit.herrencorp.com/api/v1/inbox/' + email
        response = requests.get(url = url, headers = { 'Authorization' : 'herren-recruit-python' })

        return JsonResponse({'message' : response.json()}, status = 200)
