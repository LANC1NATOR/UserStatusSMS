import time
import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

VK_AUTH_TOKEN = os.getenv('VK_AUTH_TOKEN')
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
USER_NUMBER_TO = os.getenv('USER_NUMBER_TO')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')


def get_status(user_id):
    params = {
        'user_ids': str(user_id),
        'fields': 'online',
        'v': '5.92',
        'access_token': VK_AUTH_TOKEN
    }
    user = requests.post('https://api.vk.com/method/users.get', params=params)
    user = user.json()['response']
    user_status = user[0]['online']
    return user_status


def sms_sender(sms_text):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(to=USER_NUMBER_TO,
                                     from_=TWILIO_PHONE_NUMBER,
                                     body=sms_text)
    return message.sid


if __name__ == "__main__":
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
