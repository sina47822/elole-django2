# sender.py (or wherever the send_otp function is defined)
from django.http import JsonResponse
from kavenegar import *
from django.conf import settings

from kavenegar import *
import requests

def send_telegram_message(message):
    bot_token = settings.Elole_NewBot_API_KEY  # Replace with your bot token
    chat_id = '245082791'  # Replace with your chat ID
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown',  # Optional: Change to 'HTML' if needed
    }

    response = requests.post(url, json=payload)
    return response

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
    