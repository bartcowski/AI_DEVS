import os
import openai
import base64
from dotenv import load_dotenv

load_dotenv()

map_pics = ['map1.jpg', 'map2.jpg', 'map3.jpg', 'map4.jpg']
base64_map_pics = []
for map_pic in map_pics:
  with open(map_pic, "rb") as file:
    base64_map_pics.append(base64.b64encode(file.read()).decode('utf-8'))
    print('encoded ' + map_pic)

prompt = '''
You are given 4 images, these are map fragments of some Polish cities. 

IMPORTANT INFORMATION:
- 3 of these fragments come from the same city, and one of the fragments comes from a completely different city - it is added to make it more difficult!
- in the city you are supposed to recognize there are supposedly granaries and fortresses (this must be some older, historical city then)

Based on your internal knowledge, process all of these images and try to find the name of this city from which 3 of these fragments come.

### EXAMPLE RESPONSE ###

<THOUGHTS>
what can be seen on these fragments? Take a close look at the street names, and specific objects. Remember about the clue about granaries and fortresses I gave you.
what are the most important parts that got you closer to figuring out what city it is?
If possible - which of these 4 map fragments, you think, comes from a different city?
</THOUGHTS>
<ANSWER>
name of this Polish city, nothing else
</ANSWER>

### END OF EXAMPLE RESPONSE ###
'''

gpt_client = openai.OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))
gpt_response = gpt_client.chat.completions.create(
        model="gpt-4o", # 4o instead of 4o-mini for (better?) Vision capabilities (VLM)
        messages=[
          {
            "role": "system",
            "content": "You are a detective that specializes in analyzing maps and finding locations. You have perfect vision and pay great attention to detail which makes you an expert at noticing all the important information"
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
                        "url": f"data:image/jpeg;base64,{base64_map_pics[0]}",
                        "detail": "high"
                    }
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_map_pics[1]}",
                        "detail": "high"
                    }
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_map_pics[2]}",
                        "detail": "high"
                    }
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_map_pics[3]}",
                        "detail": "high"
                    }
                }
            ]
        }],
        temperature=0.5
    )

gpt_answer = gpt_response.to_dict()['choices'][0]['message']['content']

print('\nGPT ANSWER:\n' + gpt_answer)