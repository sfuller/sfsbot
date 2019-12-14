"""
This is a very hastily thrown together script that monitors a website.
"""
import datetime
import os
from threading import Thread
from time import sleep

import requests

BOT_SECRET_TOKEN = os.environ['BOT_SECRET_TOKEN']
RECIPIENT_ID = os.environ['RECIPIENT_ID']

HI_STICKER_FILE_ID = 'CAADAQADAQADK31ZGpa0uvTmlg0xFgQ'
DOWN_STICKER_FILE_ID = 'CAADAgADDwADq2gKB8Op60pzWGnIFgQ'
UP_STICKER_FILE_ID = 'CAADBAADKAMAAqTctQLbUfI5OxTVwhYE'

SITE_URL = 'https://samfullerstudios.com'

PING_DAY_INTERVAL = 7
CHECK_MINUTE_INTERVAL = 5


def call_bot_method(http_method, method_name, form):
    r = requests.request(http_method, f'https://api.telegram.org/bot{BOT_SECRET_TOKEN}/{method_name}', data=form)
    if r.status_code != 200:
        raise ValueError(f'http {r.status_code}: {r.content}')
    return r


def send_message(text):
    call_bot_method('POST', 'sendMessage', {
        'chat_id': RECIPIENT_ID,
        'text': text
    })


def send_sticker(id):
    call_bot_method('POST', 'sendSticker', {
        'chat_id': RECIPIENT_ID,
        'sticker': id
    })


def check_site() -> str:
    status = 0
    try:
        r = requests.get(SITE_URL)
        status = r.status_code
    except:
        pass

    if status is 200:
        if os.path.exists('down'):
            os.remove('down')
            return 'back_up'
        return 'still_up'
    else:
        with open('down', 'w') as f:
            f.write('down')
        return 'down'


def checker_thread():
    while True:
        next_update_time = datetime.datetime.now() + datetime.timedelta(minutes=CHECK_MINUTE_INTERVAL)
        result = check_site()
        print(result)
        if result == 'back_up':
            send_message('The site appears to be back up! Congrats.')
            send_sticker(UP_STICKER_FILE_ID)
        elif result == 'down':
            send_message('Oh no! The site is down!!!')
            send_sticker(DOWN_STICKER_FILE_ID)
        wait(next_update_time)


def ping_thread():
    while True:
        next_ping_time = datetime.datetime.now() + datetime.timedelta(days=PING_DAY_INTERVAL)
        send_sticker(HI_STICKER_FILE_ID)
        send_message('Hi! I\'m still alive! This message is sent periodically to ensure you know I\'m still workin\'!')
        wait(next_ping_time)


def wait(time: datetime.datetime):
    while datetime.datetime.now() < time:
        sleep((time - datetime.datetime.now()).seconds)


def main():
    r = call_bot_method('GET', 'getUpdates', None)
    print(r.content)

    ping = Thread(target=ping_thread, daemon=True)
    checker = Thread(target=checker_thread, daemon=True)

    ping.start()
    checker.start()

    ping.join()
    checker.join()


if __name__ == '__main__':
    main()
