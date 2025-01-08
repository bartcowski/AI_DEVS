import glob
import whisper
import json
import requests
import os
import openai
import base64
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from aidevs_util import send_report_and_print
from gpt_util import GptService
from qdrant_util import QdrantService
from w3.t2.weapon_report import WeaponReportChunk

# python -m venv venv
# venv\Scripts\activate
# pip install requests
# pip show requests
# deactivate
#
# pip install python-dotenv
# create .env file
# load_dotenv() os.getenv('API_KEY')
#
# python -m dir1.dir2.module_name (without .py extension)
#
# pip freeze > requirements.txt

load_dotenv()
api_key = os.getenv('AI_DEVS_API_KEY')

data_url = 'https://poligon.aidevs.pl/dane.txt'

resp1 = requests.get(data_url)

soup = BeautifulSoup(resp1.content, 'html.parser')
text_content = soup.get_text()
string_array = text_content.splitlines()

answer_url = 'https://poligon.aidevs.pl/verify'
answer = {
    'task': 'POLIGON',
    'apikey': api_key,
    'answer': string_array
}

resp2 = requests.post(answer_url, json=answer)
resp2_json = resp2.json()

#access separate fields
print(f'Code: {resp2_json['code']}, Message: {resp2_json['message']}')
#pretty-print raw json
print(json.dumps(resp2_json, indent=4))