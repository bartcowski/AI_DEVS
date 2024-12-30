import whisper
import json
import requests
import os
import openai
from dotenv import load_dotenv

load_dotenv()

interrogation_files = ['adam.m4a', 'agnieszka.m4a', 'ardian.m4a', 'michal.m4a', 'monika.m4a', 'rafal.m4a']
transcription_file_names = []

model = whisper.load_model("medium")

for file_name in interrogation_files:
    base_file_name, ext = os.path.splitext(file_name)
    transcription_file_name = base_file_name + '.txt'
    transcription_file_names.append(transcription_file_name)

    if not os.path.exists(transcription_file_name):
        print('STARTED transcribing - ' + file_name)
        transcription = model.transcribe(file_name)["text"]
        with open(transcription_file_name, 'w', encoding='utf-8') as f:
            f.write(transcription)
        print('FINISHED transcribing - ' + file_name)
        
transcriptions = []
for transcription_file_name in transcription_file_names:
    print('READING transcription - ' + transcription_file_name)
    with open(transcription_file_name, 'r', encoding='utf-8') as f:
            transcriptions.append(f.read())
    print(f'No. of transcriptions - {len(transcriptions)}')

transcription_string = ''
i = 1
for transcription in transcriptions:
     transcription_string = transcription_string + 'Interrogation-' + str(i) + '\n' + transcription + '\n\n'
     i += 1

prompt = f'''
You are a detective, between <INTEROGATIONS> tags you are given transcriptions of several interrogations in polish language.
Your goal is to find the name of a Polish street, where a place at which a person named Andrzej Maj worked, or more specifically - LECTURED.
This place is a department, faculty or institue of some Polish university, we need the street on which the FACULTY is located, and NOT the main part of the university (main campus)!

NOTE that the name of this street will not be mentioned in any interrogation, you need to analyze what everybody said and based on your
internal knowledge of Polish cities and universities' faculties figure out what the exact street might be.

Return an answer in json format with two properties:
'_thoughts' - while recalling the most significant fragments of the interrogations, analyze them and create a step by step list of facts, including these ones: 
1) which city he lectured in?
2) what is the university he lectured on (e.g. MIT - Massachusetts Institute of Technology), is its mentioned in any of the interrogations?
3) what is the name of the PARTICULAR FACULTY of that university where Andrzej Maj lectured, is it also mentioned in the interrogations?
4) based on the name of the PARTICULAR FACULTY - on what street is it situated?
'street' - just the street name that you need to find, e.g. ('street': 'kupiecka'), note that it's just 'kupiecka', not 'ulica kupiecka' or 'street kupiecka' or 'ul. kupiecka'

<INTEROGATIONS>\n\n
{transcription_string}
</INTEROGATIONS>
'''

print('\n\n')
print(prompt)


gpt_client = openai.OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))
gpt_response = gpt_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3)
gpt_answer = gpt_response.to_dict()['choices'][0]['message']['content']
gpt_answer = gpt_answer.lstrip('```json\n').rstrip('```')

print('\n\nGPT ANSWER: ' + gpt_answer)

gpt_answer_dict = json.loads(gpt_answer)

report_url = 'https://centrala.ag3nts.org/report'
report = {
    'task': 'mp3',
    'apikey': os.getenv('AI_DEVS_API_KEY'),
    'answer': gpt_answer_dict['street']
}
report_response = requests.post(report_url, json=report)
print('\n\nFINAL ANSWER:')
print(report_response.text)