import json
import requests
import os
import openai
from dotenv import load_dotenv

load_dotenv()

url = 'https://centrala.ag3nts.org/data/' + os.getenv('AI_DEVS_API_KEY') + '/cenzura.txt'
resp1 = requests.get(url)

print('PERSONAL INFO: ' + resp1.text)

gpt_client = openai.OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))
gpt_prompt = f'''
You are given personal information in Polish language that you need to cenzor.
Replace name, surname, city, address, and age with the word 'CENZURA'.
After that return that cenzored string, nothing else.

Personal Information to cenzor:
{resp1.text}
'''
gpt_response = gpt_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": gpt_prompt}])
gpt_answer = gpt_response.to_dict()['choices'][0]['message']['content']

print('GPT ANSWER: ' + gpt_answer)

report_url = 'https://centrala.ag3nts.org/report'
report = {
    'task': 'CENZURA',
    'apikey': os.getenv('AI_DEVS_API_KEY'),
    'answer': gpt_answer
}
report_response = requests.post(report_url, json=report)
print(report_response.text)
