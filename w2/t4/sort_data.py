import json
import requests
import os
import openai
import base64
from dotenv import load_dotenv

load_dotenv()

txt_files = []
mp3_files = []
png_files = []

for file_name in os.listdir('./data'):
    file, ext = os.path.splitext(file_name)
    if ext == '.txt':
        txt_files.append(file_name)
        print("found TXT: " + file_name)
    elif ext == '.mp3':
        mp3_files.append(file_name)
        print("found MP3: " + file_name)
    elif ext == '.png':
        png_files.append(file_name)
        print("found PNG: " + file_name)
    else:
        print("ERROR: wrong extension " + ext)

people = []
hardware = []
def add_to_array(file_name, category):
    if category == 'PEOPLE':
        people.append(file_name)
    elif category == 'HARDWARE':
        hardware.append(file_name)
    elif category == 'NO_DATA':
        print('NO_DATA category received')
    else:
        print('ERROR: unknown category ' + category)

gpt_client = openai.OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))

print('\n\n ### PROCESSING TXT FILES ###')
file_content = ''
prompt = '''
You will be given some sort of {report_desc}. This comes from a high security factory guarded by robots.

Analyze this report thoroughly and check if it contains any information from either of these two categories:
1. PEOPLE - any info about captured or arrested people (most likely rebels) OR any info about traces or clues of their presence that were found. General mention of some people or an unsuccessful attempt at finding them does NOT apply to this category, their presence MUST be confirmed.
2. HARDWARE - any hardware fixes mentioned, these fixes most likely done to the robots guarding this factory or various equipement in and around the building. REMEBER: aplly this category to STRICTLY hardware repairs! No software updates, no repairs of software that might affect hardware but are actually fixing software of a robot.

Every report contains information from PEOPLE category, HARDWARE category or from neither of them.
If you don't find any information belonging to either of the categories classify it as NO_DATA category.

Respond in json format with TWO properties:
"_thoughts": explain what facts or fragments of the report made you classify it as a particular category
"category": PEOPLE or HARDWARE or NO_DATA, just one of these categories, nothing else

REPORT TO ANALYZE:
{file_content}
'''

for txt in txt_files:
    print('processing ' + txt)
    with open('./data/' + txt, 'r', encoding='utf-8') as f:
        content = f.read()
    prompt_with_content = prompt.format(report_desc='report written in Polish or English language', file_content=content)
    gpt_response = gpt_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt_with_content}],
        temperature=0.3)
    gpt_answer = gpt_response.to_dict()['choices'][0]['message']['content']
    gpt_answer = gpt_answer.lstrip('```json\n').rstrip('```')
    print(gpt_answer)
    print('\n\n')
    category = json.loads(gpt_answer)['category']
    add_to_array(txt, category)
    

print('\n\n ### PROCESSING MP3 FILES ###')
transcriptions = []
for mp3 in mp3_files:
    print('READING transcription - ' + mp3)
    mp3_transcription, ext = os.path.splitext(mp3)
    mp3_transcription = mp3_transcription + '.txt'
    with open(mp3_transcription, 'r', encoding='utf-8') as f:
            content = f.read()
    prompt_with_content = prompt.format(report_desc='report written in Polish or English language', file_content=content)
    gpt_response = gpt_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt_with_content}],
        temperature=0.3)
    gpt_answer = gpt_response.to_dict()['choices'][0]['message']['content']
    gpt_answer = gpt_answer.lstrip('```json\n').rstrip('```')
    print(gpt_answer)
    print('\n\n')
    category = json.loads(gpt_answer)['category']
    add_to_array(mp3, category)


print('\n\n ### PROCESSING PNG FILES ###')
for png in png_files:
    png_full_path = './data/' + png
    with open(png_full_path, "rb") as file:
        base64_png = base64.b64encode(file.read()).decode('utf-8')
    prompt_with_content = prompt.format(report_desc='PICTURE being a repair note written in Polish', file_content='<attached_image>')
    gpt_response = gpt_client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user", 
            "content": [
                {
                    "type": "text",
                    "text": prompt_with_content
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_png}",
                        "detail": "high"
                    }
                }
            ]
        }],
        temperature=0.3
    )
    gpt_answer = gpt_response.to_dict()['choices'][0]['message']['content']
    gpt_answer = gpt_answer.lstrip('```json\n').rstrip('```')
    print(gpt_answer)
    print('\n\n')
    category = json.loads(gpt_answer)['category']
    add_to_array(png, category)

people.sort()
hardware.sort()
report_url = 'https://centrala.ag3nts.org/report'
report = {
    'task': 'kategorie',
    'apikey': os.getenv('AI_DEVS_API_KEY'),
    'answer': {
        'people': people,
        'hardware': hardware
    }
}
report_response = requests.post(report_url, json=report)
print('\n\nFINAL ANSWER:')
print(report_response.text)