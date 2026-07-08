import os
import uuid

from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from services.embedding_service import generate_embedding

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
qdrant = AsyncQdrantClient(url=QDRANT_URL)
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
    try:    
        await init_qdrant()
        vector = generate_embedding(summary)
        point_id = str(uuid.uuid4())

        await qdrant.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload={"summary": summary, **metadata},
                )
            ],
        )
    except Exception as exc:
        print(f"Unable to store long-term memory: {exc}")
        return False

    return True
    
async def search_similar_memories(query_text: str, limit: int = 3):
    try:
        await init_qdrant()
        query_vector = generate_embedding(query_text)

        results = await qdrant.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            limit=limit,
            with_payload=True,
        )
        points = getattr(results, "points", results)
        return [hit.payload for hit in points if getattr(hit, "payload", None)]
    except Exception as exc:
        print(f"Unable to search long-term memory: {exc}")
        return []