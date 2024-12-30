facts_keywords_prompt = '''
You are given a text (within <TEXT> tags) in Polish language. Your task is to create a list of keywords summarizing the text:
1. First find the person that this text is mainly about - their name and surname will be the first keyword
2. Then find all the keywords that are connected with this person: profession, looks, skills, events, and everything else. Make sure you analyze the whole text.
3. If there are any other people mentioned besides the main one - ignore them

VERY IMPORTANT: 
1. All keywords must be in Polish language.
2. Keywords must be nouns in the nominative singular form (e.g., "sportowiec," not "sportowcem" or "sportowca").

The list of keywords must be in a given format:
name and surname, keyword1, keyword2, keyword3...

Do not include any explanations, introductions, or formatting — return only the keywords separated by commas.

<TEXT>
{fact}
</TEXT>
'''

report_keywords_prompt = '''
You're a specialist in extracting key information from Polish-language documents.

Your task is to: 
1. analyze the content of a report provided within <REPORT> tags and generate a list of keywords that summarize 
the report - focus mainly on what happened, what the outcome was, what was done, who or what was involved.
Provide a lot of them because these keywords will be later added as metadata to the report and make filtering and searching for this report much easier.
2. extract date and sector symbol from filename given in <REPORT_NAME> tags and ADD THEM TO KEYWORDS

VERY IMPORTANT: 
1. All keywords must be in Polish language.
2. Keywords must be nouns in the nominative singular form (e.g., "sportowiec," not "sportowcem" or "sportowca").

The list of keywords must be in a given format:
keyword1, keyword2, keyword3...

Do not include any explanations, introductions, or formatting — return only the keywords separated by commas.

<REPORT_NAME>
{report_name}
</REPORT_NAME>
<REPORT>
{report}
</REPORT>
'''

match_keywords_prompt = '''
You are given a set of keywords in Polish language withing <SOURCE> tags. 
The source keywords might mention some person (there will be a keyword with Polish name and surname).
If there is a person mentioned try to match it with a set (from <SETS> tags) of keywords about that person - the same name will also be mentioned in them.

Return all the keywords from the matched set appended to the source keywords.
The answer must be in a given format:
keyword1, keyword2, keyword3...

Remember - if the source doesn't mention ANY person return only the source keywords

<SOURCE>
{source}
</SOURCE>

<SETS>
{sets}
</SETS>
'''