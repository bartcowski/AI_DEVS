import whisper
import json
import requests
import os
import openai
from dotenv import load_dotenv

load_dotenv()

report_url = 'https://centrala.ag3nts.org/report'
report = {
    'task': 'mp3',
    'apikey': os.getenv('AI_DEVS_API_KEY'),
    'answer': 'Łojasiewicza'
}
report_response = requests.post(report_url, json=report)
print('\n\nFINAL ANSWER:')
print(report_response.text)