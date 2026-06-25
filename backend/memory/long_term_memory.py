import uuid
from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from services.embedding_service import generate_embedding

qdrant = AsyncQdrantClient(url="http://localhost:6333")
COLLECTION_NAME = "persona_long_term_memory"

async def init_qdrant():
    collections = await qdrant.get_collections()
    exists = any(c.name == COLLECTION_NAME for c in collections.collections)

    if not exists:
        await qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

async def store_memory_summary(summary: str, metadata: dict):
    vector = generate_embedding(summary)
    point_id = str(uuid.uuid4())

    await qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=point_id,
                vector=vector,
                payload={"summary": summary, **metadata}
            )
        ]
    )
    
async def search_similar_memories(query_text: str, limit: int = 3):
    query_vector = generate_embedding(query_text)

    results = await qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=limit
    )
    
    return [hit.paylaod for hit in results]