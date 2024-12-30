import requests
import os
import openai
from dotenv import load_dotenv

load_dotenv()

url = 'https://centrala.ag3nts.org/data/' + os.getenv('AI_DEVS_API_KEY') + '/robotid.json'
resp1 = requests.get(url)

robot_desc = resp1.json()['description']
print(robot_desc)

gpt_client = openai.OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))

prompt = f'''
You are given a description of a robot from a person that has seen it. Generate a concise prompt that I could give to any text-to-image model to generate an image of this robot.
Focus on its characteristics: shape, elements, looks etc., everything that matters when trying to draw an image. Mostly ignore the background, robot's actions, the person describing the robot.

### ROBOT DESCRIPTION ###
{robot_desc}
### END OF ROBOT DESCRIPTION ###
'''
gpt_response = gpt_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{
                "role": "user", 
                "content": prompt}])
gpt_answer = gpt_response.to_dict()['choices'][0]['message']['content']

print(gpt_answer)

response = gpt_client.images.generate(
  model="dall-e-3",
  prompt=gpt_answer,
  size="1024x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url

print(image_url)

report_url = 'https://centrala.ag3nts.org/report'
report = {
    'task': 'robotid',
    'apikey': os.getenv('AI_DEVS_API_KEY'),
    'answer': image_url
}
report_response = requests.post(report_url, json=report)
print('\n\nFINAL ANSWER:')
print(report_response.text)