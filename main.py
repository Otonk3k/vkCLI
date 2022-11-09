from functools import reduce
import vk
from PIL import Image
import requests
from io import BytesIO

def deep_get(dictionary, keys, default=None):
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)

actok = 'put your token here'
api = vk.API(access_token=actok, v='5.131')
conversations = api.messages.getConversations(count=3)
iter = conversations.get('items')
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