
import os
import openai
import base64
from dotenv import load_dotenv

load_dotenv()

with open('s02e02_tmp.png', "rb") as file:
    base64_pic = (base64.b64encode(file.read()).decode('utf-8'))

prompt = '''
You are given a picture of a letter written in Polish. 
Analyze the main content of the letter (black characters) - can it point to something?
If the main content points to something, what can these 5 lines of some kind of code at the end of it mean (red characters), the ones starting with A1S53?

As a professional detective - what do you think about this code? What is the message hidden behind it?

If you're not exactly sure what the message is provide extensive reasoning and clues, give further steps if possible.
'''

gpt_client = openai.OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))
gpt_response = gpt_client.chat.completions.create(
        model="gpt-4o", # 4o instead of 4o-mini for (better?) Vision capabilities (VLM)
        messages=[
          {
            "role": "system",
            "content": "You are a detective that specializes in codes, cyphers, and computer science and security. You have perfect vision and pay great attention to detail which makes you an expert at noticing patterns"
          },
          {
            "role": "user", 
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_pic}",
                        "detail": "high"
                    }
                }
            ]
        }],
        temperature=0.5
    )

gpt_answer = gpt_response.to_dict()['choices'][0]['message']['content']

print('\nGPT ANSWER:\n' + gpt_answer)