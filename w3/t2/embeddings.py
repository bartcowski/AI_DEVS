import glob
import os
from aidevs_util import send_report
from gpt_util import GptService
from qdrant_util import QdrantService
from w3.t2.weapon_report import WeaponReportChunk

qdrant = QdrantService('aidevs')
gpt = GptService()

# --- TESTING QDRANT ---
# print(f'1: {qdrant.count_points()}')
# txt = 'An apple is a fruit'
# embedding = gpt.create_embedding(txt)
# chunk = WeaponReportChunk(embedding, txt, '2024-11-11', 'example')
# qdrant_point = chunk.to_qdrant_point()
# qdrant.upsert_points([qdrant_point])
# print(f'2: {qdrant.count_points()}')
# embedding_query = gpt.create_embedding('what is an apple')
# result = qdrant.search_points(embedding_query, 1)
# print(f'3: {result}')
# print(f'4: {result[0]['report_date']}')
# qdrant.delete_all_points()
# print(f'5: {qdrant.count_points()}')

# uncomment for fresh start
# qdrant.delete_all_points()

if qdrant.count_points() == 0:
    docs = {}
    docs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'weapon_reports')
    for doc_file in glob.glob(os.path.join(docs_dir, '*.txt')):
        with open(doc_file, 'r', encoding='utf-8') as f:
            docs[os.path.basename(doc_file)] = f.read()

    qdrant_points = []
    for file_name, text in docs.items():
        embedding = gpt.create_embedding(text)
        report_date, ext = os.path.splitext(file_name)
        chunk = WeaponReportChunk(embedding, text, report_date.replace("_", "-"), 'some weapon name')
        qdrant_point = chunk.to_qdrant_point()
        qdrant_points.append(qdrant_point)

    qdrant.upsert_points(qdrant_points)

# to improve the solution I could extract the date from the file name and add it as e.g. 'Raport z dnia: 2024-12-06' directly to the report's content
query = 'W raporcie, z którego dnia znajduje się wzmianka o kradzieży prototypu broni?'
query_embedding = gpt.create_embedding(query)
result = qdrant.search_points(query_embedding, 1)
report_date = result[0]['report_date']

print(f'QDRANT RESULT: {report_date}')

send_report('wektory', report_date)