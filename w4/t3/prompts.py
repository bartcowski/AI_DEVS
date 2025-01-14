analyze_site_content_prompt = '''
You are given contents of a website within <WEBSITE> tags and a question within <QUESTION> tags.
Analyze the contents of the website and answer the given question based on the information found. 
The answer must be concise and as concrete as possible, return only this answeer and nothing else!

IMPORTANT: if there is not enough information or you just aren't sure return only NONE

<WEBSITE>
{website}
</WEBSITE>

<QUESTION>
{question}
</QUESTION>
'''

choose_link_prompt = '''
You are given a question within <QUESTION> tags and some links with brief descriptions within <LINKS> tags.
Analyze the question, then link descriptions and urls and decide which link could lead me to a site that would most likely contain information needed to answer the question.
Return only the URL (the link), nothing else. MAKE SURE YOU 

<LINKS>
{links}
</LINKS>

<QUESTION>
{question}
</QUESTION>
'''