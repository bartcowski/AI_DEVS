import os
from aidevs_util import send_report_and_print
from gpt_util import GptService

working_dir = os.path.dirname(os.path.abspath(__file__))
verify_data_f = os.path.join(working_dir, 'verify.txt')

gpt = GptService()

correct_ids = []
with open(verify_data_f, 'r') as f:
    for line in f:
        print(f'processing line {line}')
        id_to_numbers_tuple = line.strip().split('=')
        id = id_to_numbers_tuple[0]
        numbers = id_to_numbers_tuple[1]

        gpt_resp = gpt.user_completion(numbers, model='ft:gpt-4o-mini-2024-07-18:personal:ai-devs-numbers:Ana64Iqg')
        print(f'Q: [{numbers}], A: [{gpt_resp}]')

        if gpt_resp == 'CORRECT':
            correct_ids.append(id)

print(f'sending ids: {correct_ids}')
send_report_and_print('research', correct_ids)