from aidevs_util import send_report, database_request
from neo4j_util import Neo4jService

neo4j = Neo4jService()

# neo4j.delete_everything()

users_query = 'SELECT id, username from users'
connections_query = 'SELECT * from connections'

if neo4j.count_nodes() == 0:
    users = {}
    users_resp = database_request('database', users_query)
    for user in users_resp['reply']:
        neo4j.create_node('Person', {'name': user['username']})
        users[user['id']] = user['username']
    neo4j.count_nodes()

    connections = []
    connections_resp = database_request('database', connections_query)
    for connection in connections_resp['reply']:
        name1 = users[connection['user1_id']]
        name2 = users[connection['user2_id']]
        neo4j.run_query(f"MATCH (a:Person {{name: '{name1}'}}), (b:Person {{name: '{name2}'}}) CREATE (a)-[:KNOWS]->(b)")

path = neo4j.run_shortestpath_Rafal_Barbara_query()
print(f'\nFINAL PATH: {path}')
send_report('connections', path)