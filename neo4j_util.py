import os
from dotenv import load_dotenv
from neo4j import Driver, GraphDatabase

class Neo4jService:
    driver: Driver

    def __init__(self):
        print('[neo4j] instantiatiating service...')
        load_dotenv()
        self.driver = GraphDatabase.driver(
            os.getenv('NEO4J_URI'), 
            auth=(os.getenv('NEO4J_USERNAME'), os.getenv('NEO4J_PASSWORD')))
        
    def __del__(self):
        print('[neo4j] closing the driver')
        self.driver.close()

    def run_query(self, query):
        with self.driver.session() as session:
          print(f'[neo4j] running query: {query}')
          session.run(query)
        
    def create_node(self, label, properties):
       query = f'CREATE (n:{label} $properties)'
       with self.driver.session() as session:
          session.run(query, properties=properties)
          print(f'[neo4j] added node {label} {properties}')

    def count_nodes(self):
        query = 'MATCH (n) RETURN COUNT(n) AS node_count'
        with self.driver.session() as session:
            result = session.run(query)
            count = result.single()['node_count']
            print(f'[neo4j] counted {count} nodes')
            return count
    
    def delete_everything(self):
       query = 'MATCH (n) DETACH DELETE n'
       with self.driver.session() as session:
          session.run(query)
          print('[neo4j] everything deleted')

    def run_shortestpath_Rafal_Barbara_query(self):
        shortest_path_query = '''
        MATCH (a:Person {name: 'Rafał'}), (b:Person {name: 'Barbara'})
        MATCH p = shortestPath((a)-[*]-(b))
        RETURN [n IN nodes(p) | n.name] AS names
        '''
        with self.driver.session() as session:
          print(f'[neo4j] running shortest path query between Rafał and Barbara nodes')
          shortest_path_result = session.run(shortest_path_query).single()
          if shortest_path_result:
           return ", ".join(shortest_path_result['names'])
          else:
            raise Exception("No shortest path was found!")
    
    # TODO: does not work (Parameter maps cannot be used in `MATCH` patterns)
    # def create_relationship(self, node1_label, node1_props, node2_label, node2_props, relationship, relationship_props = {}):
    #    query = f'MATCH (a:{node1_label} $node1_props), (b:{node2_label} $node2_props) CREATE (a)-[:{relationship} $relationship_props]->(b)'
    #    with self.driver.session() as session:
    #       session.run(query, node1_props=node1_props, node2_props=node2_props, relationship_props=relationship_props)