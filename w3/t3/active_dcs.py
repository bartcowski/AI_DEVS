from aidevs_util import send_report_and_print, database_request
from gpt_util import GptService

# --- AI_DEVS DB MANUAL TESTS ---
# query1 = '''
# select dc_id from datacenters where is_active=1 AND manager in (select id from users where is_active=0)
# '''
# query2 = '''
# SELECT dc.dc_id 
# FROM datacenters dc 
# INNER JOIN users u ON dc.manager = u.id 
# WHERE dc.is_active=1 AND u.is_active=0
# '''
# resp = database_request('database', query2)
# arr = [obj['dc_id'] for obj in resp['reply']]
# print(arr)
# send_report('database', arr)

gpt = GptService()

tables_query = 'show tables'
tables_resp = database_request('database', tables_query)
tables = [x['Tables_in_banan'] for x in tables_resp['reply']]

tables_desc = []
for table in tables:
    table_desc_resp = database_request('database', f'desc {table}')
    arr = [{key: x[key] for key in ['Field', 'Type']} for x in table_desc_resp['reply']]
    tables_desc.append(arr)

tables_and_desc = []
for i in range(len(tables)):
    tables_and_desc.append({tables[i]: tables_desc[i]})

prompt = f'''
You are an expert when it comes to relational databases and SQL queries.

Within <STRUCTURE> tags you're given database tables with their columns (name and its type).
Analyze it and produce SQL query that would give me: IDs of active data centers which are assigned to managers that are currently on a leave (are inactive)

<STRUCTURE>
{tables_and_desc}
</STRUCTURE>

Return only the SQL query, nothing else
'''
query_from_gpt = gpt.user_completion_sql(prompt)

print(query_from_gpt)

dc_ids_resp = database_request('database', query_from_gpt)
arr = [x['dc_id'] for x in dc_ids_resp['reply']]
print(arr)
send_report_and_print('database', arr)