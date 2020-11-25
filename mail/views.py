import json
import re

from django.views import View
from django.http import JsonResponse

from .models import Address

class SubscribeView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            input_name = data['name']
            input_email = data['email']

            is_email_form = re.compile('[@]((\.)|(([\w-]+\.)+))')
            if not(is_email_form.search(input_email)):
                return JsonResponse({'message' : 'WRONG_EMAIL_FORMAT'}, status = 400)

            Address(
                name = input_name,
                email = input_email
            ).save()
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
        return JsonResponse({'message' : 'REGIST_SUCCESS'}, status = 200)

class UnsubscribeView(View):
    def delete(self, request):
        try:
            data = json.loads(request.body)
            
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
