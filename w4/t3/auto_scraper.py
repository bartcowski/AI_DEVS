import requests
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from aidevs_util import send_report_and_print
from gpt_util import GptService
from .prompts import analyze_site_content_prompt, choose_link_prompt

load_dotenv()
questions = requests.get(f'https://centrala.ag3nts.org/data/{os.getenv('AI_DEVS_API_KEY')}/softo.json').json()
print(f'questions received: {questions}')

gpt = GptService()
main_url = 'https://softo.ag3nts.org'

def extract_links_from_soup(soup):
    result = []
    a_tags = soup.find_all('a')
    for a_tag in a_tags:
        href = a_tag.get('href')
        if 'http' not in href:
            href = main_url + href
        result.append(f'{href} ({a_tag.get('title')} {a_tag.get_text()})')
    return result

answers = {}
for question_id in questions:
    print(f'processing question {question_id}: {questions[question_id]}')
    current_url = main_url
    gpt_answer = 'NONE'
    while gpt_answer == 'NONE':
        print(f'processing url: {current_url}')
        site = requests.get(current_url)
        soup = BeautifulSoup(site.content, 'html.parser')
        text_content = soup.get_text()
        links = extract_links_from_soup(soup)

        full_site_content = text_content + ", ".join(links)
        gpt_answer = gpt.user_completion(analyze_site_content_prompt.format(website=full_site_content, question=questions[question_id]))
        print(f'gpt answer: {gpt_answer}')
        if gpt_answer != 'NONE':
            break

        # this website is simple, but with ones that are more complex there would need to be a way to go back to previous websites (e.g. after an arbitrary number of iterations? seems difficult)
        # only going deeper might fail if the first chosen link was wrong
        next_url = gpt.user_completion(choose_link_prompt.format(links=links, question=questions[question_id]))
        print(f'next site: {next_url}')
        current_url = next_url
    
    answers[question_id] = gpt_answer
    print(f'answer: {answers[question_id]}')

print(f'\n\nFINAL ANSWERS:\n {answers}')
send_report_and_print('softo', answers)