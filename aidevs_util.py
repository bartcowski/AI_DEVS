import os
from dotenv import load_dotenv
import requests

def send_report(task, answer):
    load_dotenv()
    report_url = 'https://centrala.ag3nts.org/report'
    report = {
        'task': task,
        'apikey': os.getenv('AI_DEVS_API_KEY'),
        'answer': answer
    }
    report_response = requests.post(report_url, json=report)
    print(f'\n\nREPORT RESULT:\n{report_response.text}')

def database_request(task, query) -> dict:
    load_dotenv()
    report_url = 'https://centrala.ag3nts.org/apidb'
    report = {
        'task': task,
        'apikey': os.getenv('AI_DEVS_API_KEY'),
        'query': query
    }
    report_response = requests.post(report_url, json=report)
    return report_response.json()