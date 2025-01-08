prompt = 'This is a prompt'

base64_images = ['aaa', 'bbb', 'ccc']

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

    
messages={
            "role": "user", 
            "content": content
        }

print(messages)