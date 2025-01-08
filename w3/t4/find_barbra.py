import unicodedata
import requests
import os
from bs4 import BeautifulSoup
from aidevs_util import people_request, places_request, send_report_and_print
from gpt_util import GptService

### HANDLE THE NOTE AND EXTRACT INITIAL NAMES
note_url = 'https://centrala.ag3nts.org/dane/barbara.txt'
note_resp = requests.get(note_url)
soup = BeautifulSoup(note_resp.content, 'html.parser')
note_content = soup.get_text()

note_names_file_path = os.path.dirname(os.path.abspath(__file__)) + '/note_names.txt'
initial_names = []
if os.path.exists(note_names_file_path):
    with open(note_names_file_path, 'r') as f:
        initial_names = f.read().split(", ")
else:
    extract_names_prompt = f'''
    You are given a note written in Polish, find all distinct FIRST NAMES from this note and return them in NOMINATIVE form.
    Return all first names separated by commas and NOTHING ELSE.

    <NOTE>
    {note_content}
    </NOTE>

    <EXAMPLES>
    Ewa Polak -> Ewa
    Piotrowi Nowakowi -> Piotr
    Kazimierzem Kowalskim -> Kazimierz
    Pawła Mareckiego -> Pawel
    </EXAMPLES>

    <RETURN FORMAT>
    Ewa, Piotr, Kazimierz, Pawel
    </RETURN FORMAT>
    '''
    gpt = GptService()
    names_from_gpt = gpt.user_completion(extract_names_prompt)

    def remove_diacritics(text):
        text = text.replace('ł', 'l').replace('Ł', 'L')
        return ''.join(c for c in unicodedata.normalize('NFD', text) 
                    if unicodedata.category(c) != 'Mn')
    names_without_diacritics = remove_diacritics(names_from_gpt)

    with open(note_names_file_path, 'w') as f:
        f.write(names_without_diacritics.upper())
    initial_names = names_without_diacritics.split(", ")

print(f'INITIAL NAMES: {initial_names}')

### FIND BARBRA
people = set(initial_names)
places = set()
barbra_locations = []
for i in range(0, 50):
    print(f'====== STEP {i} ======')

    people_len = len(people)
    places_len = len(places)

    for name in people:
        new_places_json = people_request(name)
        print(f'--- {new_places_json['message']}')
        if new_places_json['code'] == 0 and 'RESTRICTED DATA' not in new_places_json['message']:
            places.update(new_places_json['message'].split(' '))

    for place in places:
        new_people_json = places_request(place)
        print(f'--- {new_people_json['message']}')
        if new_people_json['code'] == 0 and 'RESTRICTED DATA' not in new_people_json['message']:
            if 'BARBARA' in new_people_json['message'] and place not in barbra_locations:
                barbra_locations.append(place)
            people.update(new_people_json['message'].split(' '))

    if people_len == len(people) and places_len == len(places):
        break
    
    print(f'people = {people}')
    print(f'places = {places}')

print(f'BARBRA LOCATIONS: {barbra_locations}')
send_report_and_print('loop', barbra_locations[-1])