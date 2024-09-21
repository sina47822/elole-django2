# sender.py (or wherever the send_otp function is defined)
from django.http import JsonResponse
from kavenegar import *
from django.conf import settings

from kavenegar import *

def send_otp(otp):
    api = KavenegarAPI(settings.KAVENEGAR_API_KEY)
    params = {
        'receptor': otp.receiver,
        'type': 'sms',
        'template': 'verify',  # Kavenegar template name
        'token': {otp.password}  # Generate and use the token
    }

    try:
        api.verify_lookup(params)  # Ensure this method is supported
    except APIException as e:
        print(f"APIException: {e}")
    except HTTPException as e:
        print(f"HTTPException: {e}")
    