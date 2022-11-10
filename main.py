from functools import reduce
import vk
from PIL import Image
import requests
from io import BytesIO
from random import randint

def deep_get(dictionary, keys, default=None):
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)

actok = 'vk1.a.ofVCQOiI7ZPwr7yo1hGHwKYeVuvL0zCbJDgJrf0xB5JqPrVr0JNQqLq_T0ppwESoeKOGFPuRIAmYUg-4KWDyvAlXbeCkPg5V2AQ6RrfrM0Z4Bc89E3QYd3wu-zzyI5gPEaZzBE97HzNDZwCG5yixYLxFh9BMYOZDdg4GOLgCOkiKc9QDctdytPbdHDBk_2X2IJMhdTpEIXMRZ326_ywadg'
api = vk.API(access_token=actok, v='5.131')
conversations = api.messages.getConversations(count=3)
iter = conversations.get('items')

def get_messages():
    for i in iter:
        ides = deep_get(i, 'conversation.peer.id')
        unread_counter = deep_get(i, 'conversation.unread_count')
        print(ides, unread_counter)

        dirty_messages = api.messages.getHistory(count=4, user_id=ides)
        for ii in dirty_messages.get('items'):
            if ii.get('attachments'):
                for attachments in deep_get(ii, 'attachments'):
                    print(attachments.get('type'))
                    if attachments.get('type') == 'video':
                        for each_video_attached in deep_get(attachments, 'video.stats_pixels'):
                            print(each_video_attached.get('url'))
                    elif attachments.get('type') == 'photo':
                        for each_photo in deep_get(attachments, 'photo.sizes'):
                            if '604x516' in each_photo.get('url'):
                                photo_preview = requests.get(each_photo.get('url'))
                                img = Image.open(BytesIO(photo_preview.content))
                                print(img.show())


            else:
                print('\n', ii.get('text'))

def get_dialogs(count):
    dialogs = api.messages.getConversations(count=count)
    iter = 1
    for i in dialogs.get('items'):
        id = deep_get(i, 'conversation.peer.id')
        if id < 2000000000 and id > 0:
            user = api.users.get(user_ids=id)
            for us in user:
                print(iter, us.get('first_name'), us.get('last_name'), '(', us.get('id'), ')')
        elif id > 2000000000:
            message = api.messages.getConversationsById(peer_ids=id)
            for thing in message.get('items'):
                print(iter, deep_get(thing, 'chat_settings.title'), '(', deep_get(thing, 'peer.id'), ')')
        elif id < 0:
            id *= -1
            group = api.groups.getById(group_id=id)
            for g in group:
                print(iter, g.get('name'), '(', g.get('id'), ')')
        iter += 1

def send_messages():
    get_dialogs(10)
    dialog = input("input dialog id: ")
    message = input("Enter message to send: ")
    api.messages.send(peer_id=dialog, message=message, random_id=randint(-2147483648, 2147483647)) #random_int is unique int32

send_messages()