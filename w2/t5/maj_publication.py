import json
import requests
import os
import openai
import base64
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dotenv import load_dotenv

import whisper_util

load_dotenv()
gpt_client = openai.OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))

questions_url = 'https://centrala.ag3nts.org/data/2a0df61b-862c-4833-a94b-6d263c36e8b8/arxiv.txt'
publication_url = 'https://centrala.ag3nts.org/dane/arxiv-draft.html'

publication = requests.get(publication_url)
soup = BeautifulSoup(publication.content, 'html.parser')

### handle mp3 recording
recording_source = soup.find('source')
recording_url = recording_source.get('src')
recording_full_url = urljoin(publication_url, recording_url)
recording_file_name = os.path.basename(recording_full_url)
if not os.path.exists(recording_file_name):
    recording_content = requests.get(recording_full_url).content
    with open(recording_file_name, 'wb') as f:
        f.write(recording_content)

transcription = whisper_util.transcribeOrRead(recording_file_name)
recording_source.replace_with('[transcription] ' + transcription + ' [end of transcription]')

### handle images
images = soup.find_all('img')
for img in images:
    img_src = img.get('src')
    img_full_url = urljoin(publication_url, img_src)
    caption = img.find_next('figcaption').get_text(strip=True)

    img_content = requests.get(img_full_url).content
    base64_img = base64.b64encode(img_content).decode('utf-8')
    prompt = f'''
Provide a concise description of a given image, it shouldn't be more than 2 or 3 sentences. I want the description TO BE IN POLISH LANGUAGE.
You're given a caption in Polish that was placed below the image to provide some context that might be useful to better understand the contents of the image.
CAPTION: {caption}
'''
    gpt_response = gpt_client.chat.completions.create(
        model="gpt-4o",
        messages=[{
            "role": "user", 
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_img}",
                        "detail": "high"
                    }
                }
            ]
        }],
        temperature=0.5
    )
    gpt_answer = gpt_response.to_dict()['choices'][0]['message']['content']
    img.replace_with('[img description] ' + gpt_answer + ' [end of img description]')
    
# retrieving whole publication with images replaced with descriptions and audio recordings replaced with transcriptions as TEXT
publication_txt = soup.get_text()

questions_raw = requests.get(questions_url)
soup = BeautifulSoup(questions_raw.content, 'html.parser')
questions_txt = soup.get_text()

prompt = f'''
You are given a long scientific publication between <PUBLICATION> tags, it is written in Polish language.
It originally contained images and audio recordings but these were replaced with text to make sure you can process it without problems. 
Both descriptions and transcriptions were placed in the same spots in the publication as the original media - remember that because surrounding paragraphs might be important sources of context.

Image descriptions look like this: [img description] some description of an image [end of img description]
Audio recording transcriptions look like this: [transcription] some transcription [end of transcription]

On top of that you're given some questions, between <QUESTIONS> tags - also in Polish. You need to answer them BASED ON THE INFORMATION FOUND IN THE PUBLICATION.
DO NOT try to guess anything, find all the necessary data in the publication, and answer the questions concisely.
DO NOT write too long of an answer for each question, these will be rather simple and 1 sentence will suffice.
EVERY ANSWER MUST BE IN POLISH LANGUAGE.

Your response must be in a following JSON format:
<RESPONSE_FORMAT>
{{
    "question_id": "1 sentence answer",
    "question_id": "1 sentence answer",
    "question_id": "1 sentence answer",
    ...
}}
</RESPONSE_FORMAT>

so for example you might be given one question, between the tags I mentioned before:
04=what is the capital of Poland?
and your answer should be:
{{
    "04": "The capital of Poland is Warsaw"
}}

<PUBLICATION>
{publication_txt}
</PUBLICATION>

<QUESTIONS>
{questions_txt}
</QUESTIONS>
'''
gpt_response = gpt_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3)
gpt_answer = gpt_response.to_dict()['choices'][0]['message']['content']
gpt_answer = gpt_answer.lstrip('```json\n').rstrip('```')
print(gpt_answer)
print('\n\n')

json_answers = json.loads(gpt_answer)

report_url = 'https://centrala.ag3nts.org/report'
report = {
    'task': 'arxiv',
    'apikey': os.getenv('AI_DEVS_API_KEY'),
    'answer': json_answers
}
report_response = requests.post(report_url, json=report)
print('\n\nFINAL ANSWER:')
print(report_response.text)