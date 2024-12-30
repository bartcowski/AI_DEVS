import json
import requests
import os
import openai
from dotenv import load_dotenv

load_dotenv()

if not os.path.exists('data_3.json'):
    url = 'https://centrala.ag3nts.org/data/' + os.getenv('AI_DEVS_API_KEY') + '/json.txt'
    resp1 = requests.get(url)
    with open('data_3.json', 'w', encoding='utf-8') as f:
        json.dump(resp1.json(), f, ensure_ascii=False, indent=4)

with open('data_3.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    print('json file loaded')

data['apikey'] = os.getenv('AI_DEVS_API_KEY')
gpt_client = openai.OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))

for element in data['test-data']:
    question = element["question"]
    left_operand, right_operand = map(int, question.split(" + "))
    element['answer'] = left_operand + right_operand

    if 'test' in element:
        gpt_prompt = f'''
            Anwer the question below, give me only that answer, nothing else.
            {element['test']['q']}
            '''
        gpt_response = gpt_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": gpt_prompt}])
        gpt_answer = gpt_response.to_dict()['choices'][0]['message']['content']
        element['test']['a'] = gpt_answer
        print("Q: " + element['test']['q'])
        print("A: " + gpt_answer)

print('finished fixing the data, sending the report...')

report_url = 'https://centrala.ag3nts.org/report'
report = {
    'task': 'JSON',
    'apikey': os.getenv('AI_DEVS_API_KEY'),
    'answer': data
}
report_response = requests.post(report_url, json=report)
print(report_response.text)