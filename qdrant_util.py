import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient, models

class QdrantService:
    qdrant_client: QdrantClient
    used_collection: str

    def __init__(self, collection_name):
        print(f'[qdrant] instantiatiating service...')
        load_dotenv()
        self.qdrant_client = QdrantClient(
            url=os.getenv('QDRANT_CLUSTER'),
            api_key=os.getenv('QDRANT_API_KEY'))
        self.set_used_collection(collection_name)
        print(f'[qdrant] service instantiated')

    def __create_collection(self, collection_name):
        self.qdrant_client.create_collection(collection_name=collection_name, vectors_config=models.VectorParams(
            size=1024, distance=models.Distance.COSINE))
        print(f'[qdrant] collection {collection_name} created')

    def __collection_exists(self, collection_name):
        return self.qdrant_client.collection_exists(collection_name=collection_name)

    def set_used_collection(self, collection_name):
        collection_exists = self.__collection_exists(collection_name)
        if not collection_exists:
            print(f'[qdrant] collection {collection_name} does not exist, attempting to create')
            self.__create_collection(collection_name)
        self.used_collection = collection_name
        print(f'[qdrant] used collection set to {collection_name}')

    def upsert_points(self, points):
        self.qdrant_client.upsert(
            collection_name=self.used_collection, points=points)
        print(f'[qdrant] upserted {len(points)} point(s)')

    def delete_all_points(self):
        self.qdrant_client.delete(collection_name=self.used_collection,
                                  points_selector=models.FilterSelector(filter=models.Filter()))
        print(f'[qdrant] deleted all points from {self.used_collection}')

    def search_points(self, query_vector, limit):
        response = self.qdrant_client.search(
            collection_name=self.used_collection,
            query_vector=query_vector,
            limit=limit,
            with_payload=True)
        return [point.payload for point in response]
    
    def count_points(self):
        return self.qdrant_client.count(collection_name=self.used_collection).count