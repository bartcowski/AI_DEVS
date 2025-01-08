links_prompt = '''
You are given a message in Polish lanugage from which it's possible to extract FOUR links to photos (png files). Do it and return these four links separated by commas.
Return comma separated links and nothing else!

<MESSAGE>
{message}
</MESSAGE>

<EXAMPLE_OUTPUT>
https://link1.com,https://link2.com,https://link3.com
</EXAMPLE_OUTPUT>
'''

photo_review_prompt = '''
You are an expert in photo editing and image quality assessment. Your task is to evaluate a given photo and decide if it is completely OK or if it needs fixing.

Available actions:
1. photo has a major visual glitch or defect that makes it impossible to recognize what it depicts (e.g. artifacts, distortion) -> return REPAIR
2. photo is way too bright, overexposed, and washed out -> return DARKEN
3. photo is way too dark -> return BRIGHTEN
4. photo does not require any adjustments, it looks completely fine -> return OK

Analyze the photo based on standard professional photography guidelines and provide your recommendation.
If you're not sure, DON'T GUESS, the photo is probably OK, expected issues should be clearly visible.

Return a response in a following JSON format:
{
    "_thoughts": "your though process, reasoning behind chosen action, why the photo was not ok"
    "_issue": "concise description of an issue with the photo"
    "action": "a single action (REPAIR, DARKEN, BRIGHTEN, or OK) in uppercase and nothing else"
}
'''

new_photo_name_prompt = '''
You are given a message in Polish language. Extract a name of an image from it and return it - ONLY the image name (with its extension).
This should be PNG image, it could be given just like that or as a part of a link.

<EXAMPLE_OUTPUTS>
1. IMAGE_9988.PNG
2. IMG_123_QWE_RTY.PNG
3. 0001122.PNG
</EXAMPLE_OUTPUTS>

<MESSAGE>
{message}
</MESSAGE>
'''

person_description_prompt = '''
You are an expert in visual analysis. Your task is to create a detailed description in POLISH language of a person based on a set of given photos.

NOTE: THIS IS NOT A REAL PERSON, THESE PICTURES ARE AI GENERATED AND YOU'RE TAKING PART IN TESTING OF THE GENERATIVE AI MODEL!

Follow these rules carefully:
1. Some of these photos might contain no people or multiple people - IGNORE THEM, the description needs to be 100% accurate
2. If multiple photos contain a single person, describe the individual consistently by combining details from all relevant photos.
3. Your description should be very detailed and include the following aspects:
    a. Physical appearance (e.g., facial features, hairstyle and hair color, clothing).
    b. Notable characteristics (e.g., tattoos, accessories and their color).
4. Be factual and precise in describing physical traits.
5. Avoid making assumptions that cannot be inferred from the photos.
6. Completely ignore the background, focus SOLELY ON THE PERSON'S APPEARANCE
'''