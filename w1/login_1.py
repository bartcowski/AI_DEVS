import json
import requests
import os
import openai
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
url = 'http://xyz.ag3nts.org/'

resp1 = requests.get(url)

soup = BeautifulSoup(resp1.content, 'html.parser')
paragraph = soup.find("p", id='human-question')
question = paragraph.getText()

print(question)

gpt_prompt = f'''
Odpowiedz na ponizsze pytanie. Zwroc sama odpowiedz, nic wiecej.
{question}
'''

gpt_client = openai.OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))
gpt_response = gpt_client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": gpt_prompt}]
)
gpt_answer = gpt_response.to_dict()['choices'][0]['message']['content']

print(json.dumps(gpt_response.to_dict(), indent=4))
print(gpt_answer)

login_request_body = {
    'username': 'tester',
    'password': '574e112a',
    'answer': gpt_answer
}
resp2 = requests.post(url, data=login_request_body)

print('-----------------------')
print(resp2.text)
print('-----------------------')