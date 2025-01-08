import json
import openai
import os
from dotenv import load_dotenv

class GptService:
    def __init__(self):
        load_dotenv()
        self.__gpt_client = openai.OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))

    def user_completion(self, prompt, model='gpt-4o-mini', temperature=0.5):
        gpt_response = self.__gpt_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return gpt_response.to_dict()['choices'][0]['message']['content']

    def user_completion_json(self, prompt, model='gpt-4o-mini', temperature=0.5):
        gpt_response = self.__gpt_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        gpt_answer = gpt_response.to_dict()['choices'][0]['message']['content']
        gpt_answer = gpt_answer.lstrip('```json\n').rstrip('```')
        return json.loads(gpt_answer)
    
    def user_completion_sql(self, prompt, model='gpt-4o-mini', temperature=0.5):
        gpt_response = self.__gpt_client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        gpt_answer = gpt_response.to_dict()['choices'][0]['message']['content']
        return gpt_answer.lstrip('```sql\n').rstrip(';```')
    
    def user_completion_with_image(self, prompt, base64_image, model='gpt-4o', temperature=0.5):
        gpt_response = self.__gpt_client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user", 
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                        "detail": "high"
                    }
                }
            ]
        }],
        temperature=temperature
        )
        return gpt_response.to_dict()['choices'][0]['message']['content']
    
    def user_completion_json_with_image(self, prompt, base64_image, model='gpt-4o', temperature=0.5):
        gpt_response = self.__gpt_client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user", 
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                        "detail": "high"
                    }
                }
            ]
        }],
        temperature=temperature
        )
        gpt_answer = gpt_response.to_dict()['choices'][0]['message']['content']
        gpt_answer = gpt_answer.lstrip('```json\n').rstrip('```')
        return json.loads(gpt_answer)
    
    def user_completion_with_images(self, prompt, base64_images, model='gpt-4o', temperature=0.5):
        content = []
        content.append({
                    "type": "text",
                    "text": prompt
                    })
        for base64_image in base64_images:
            content.append({
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}",
                        "detail": "high"
                        }
                    })

        gpt_response = self.__gpt_client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user", 
            "content": content
        }],
        temperature=temperature
        )
        return gpt_response.to_dict()['choices'][0]['message']['content']

    def create_embedding(self, input, dimensions=1024):
        response = self.__gpt_client.embeddings.create(
            model='text-embedding-3-small',
            input=input,
            dimensions=dimensions
        )
        return response.to_dict()['data'][0]['embedding']