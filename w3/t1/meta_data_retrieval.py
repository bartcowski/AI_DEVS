import glob
import requests
import os
from dotenv import load_dotenv
from gpt_util import GptService
from .prompts import facts_keywords_prompt, report_keywords_prompt, match_keywords_prompt

load_dotenv()
gpt_client = GptService()


facts = []
facts_keywords = []
reports = {}


# load facts
facts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'facts')
for fact_file in glob.glob(os.path.join(facts_dir, '*.txt')):
    with open(fact_file, 'r', encoding='utf-8') as f:
        facts_content = f.read()
        if 'entry deleted' not in facts_content:
            facts.append(facts_content)
print('loaded fact files')


# load reports
reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'reports'))
for report_file in glob.glob(os.path.join(reports_dir, '*.txt')):
    filename = os.path.basename(report_file)
    with open(report_file, 'r', encoding='utf-8') as f:
        reports[filename] = f.read()
print('loaded report files')


# create facts keywords
for fact in facts:
    facts_keywords_prompt_formatted = facts_keywords_prompt.format(fact=fact)
    gpt_answer = gpt_client.user_completion(facts_keywords_prompt_formatted)
    person = gpt_answer.split(',')[0]
    facts_keywords.append(f'{person}: [{gpt_answer}]')
    print('\n---------------------------------------------')
    print(f'{person}: [{gpt_answer}]')


# create metadata
metadata = {}
for report_name in reports.keys():
    report_keywords_prompt_formatted = report_keywords_prompt.format(report_name=report_name, report=reports[report_name])
    gpt_answer = gpt_client.user_completion(report_keywords_prompt_formatted)
    print('\n---------------------------------------------')
    print(f'{report_name} : {gpt_answer}')

    match_keywords_prompt_formatted = match_keywords_prompt.format(source=gpt_answer, sets=facts_keywords)
    gpt_answer = gpt_client.user_completion(match_keywords_prompt_formatted)
    metadata[report_name] = gpt_answer
    print('\n---------------------------------------------')
    print(f'FINAL: {report_name} : {gpt_answer}')


report_url = 'https://centrala.ag3nts.org/report'
report = {
    'task': 'dokumenty',
    'apikey': os.getenv('AI_DEVS_API_KEY'),
    'answer': metadata
}
report_response = requests.post(report_url, json=report)
print('\n\nFINAL ANSWER:')
print(report_response.text)