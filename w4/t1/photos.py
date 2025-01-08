import requests
import os
import base64
from aidevs_util import send_report, send_report_and_print
from gpt_util import GptService
from .prompts import links_prompt, photo_review_prompt, new_photo_name_prompt, person_description_prompt

gpt = GptService()

start_response = send_report('photos', 'START')
print(start_response['message'])

# regex would be way more complicated, the links are returned in different ways, they're sometimes divided into parts
links_from_gpt = gpt.user_completion(links_prompt.format(message=start_response['message']))
links = links_from_gpt.split(',')
print(f'retrieved {len(links)} photo links')

class Photo:
    name: str
    base64_photo: bytes
    is_ok: bool

    def __init__(self, name, base64_photo, is_ok):
        self.name = name
        self.base64_photo = base64_photo
        self.is_ok = is_ok

photos = []
base_url, _ = os.path.split(links[0])

print(f'photos base url: {base_url}')

# initialize photos 
for link in links:
    _, photo_name = os.path.split(link)
    photo_content = requests.get(link).content
    base64_photo = base64.b64encode(photo_content).decode('utf-8')
    photos.append(Photo(photo_name, base64_photo, False))
    print(f'init photo {photo_name}')

def all_photos_ok(photos):
    return all(photo.is_ok for photo in photos)

# run loop until all photos are marked as ok (or too many iterations $$$)
iterations = 0
while not all_photos_ok(photos) and iterations < 5:
    new_photos = []
    photo_names_to_delete = []

    print(f'LOOP processing {len(photos)} photos')

    for photo in photos:
        if photo.is_ok:
            print(f'photo {photo.name} is already ok, skipping...')
            continue

        gpt_assessment = gpt.user_completion_json_with_image(photo_review_prompt, photo.base64_photo, temperature=0.0)

        print(f'GPT assessment for {photo.name}: {gpt_assessment}')
        assert gpt_assessment['action'] in ['OK', 'REPAIR', 'DARKEN', 'BRIGHTEN'], f'unknown action from GPT: {gpt_assessment['action']}'
        
        if gpt_assessment['action'] == 'OK':
            photo.is_ok = True
            print(f'photo {photo.name} marked as OK')
            continue
        
        # what if HERE it turns out that the action is not correct? 
        # GPT should analyze this response and if it does not find a file (or sees that something went wrong) 
        # I should add this action to 'taken_actions' in Photo object and present them to GPT in photo_review_prompt so that it can choose something else next time
        print(f'sending [{gpt_assessment['action']} {photo.name}]')
        new_photo_message = send_report('photos', f'{gpt_assessment['action']} {photo.name}')['message']
        print(f'received response: {new_photo_message}')
        new_photo_name = gpt.user_completion(new_photo_name_prompt.format(message=new_photo_message))
        print(f'extracted new photo: {new_photo_name}')

        full_photo_url = base_url + '/' + new_photo_name
        new_photo_content = requests.get(full_photo_url).content
        new_base64_photo = base64.b64encode(new_photo_content).decode('utf-8')
        new_photos.append(Photo(new_photo_name, new_base64_photo, False))
        photo_names_to_delete.append(photo.name)

    print(f'LOOP {len(photo_names_to_delete)} to delete and {len(new_photos)} new ones')
    photos = [photo for photo in photos if photo.name not in photo_names_to_delete]
    photos.extend(new_photos)
    iterations += 1

print(f'\n\nFINAL PHOTOS: {[photo.name for photo in photos]}')
assert len(photos) == len(links), 'after repairs there should be as many photos as in the beginning'

base64_photos = [photo.base64_photo for photo in photos]
description = gpt.user_completion_with_images(person_description_prompt, base64_photos, temperature=0.3)
print(f'\n\nGENERATED DESCRIPTION: {description}')

send_report_and_print('photos', description)