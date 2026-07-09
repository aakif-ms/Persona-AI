import os
import re

from neo4j import AsyncGraphDatabase

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password123")


def _sanitize_relationship(relation: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_]", "_", relation.upper()).strip("_")
    return cleaned or "RELATED_TO"

class SemanticMemory:
    def __init__(self):
        self.driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    async def close(self):
        await self.driver.close()
    
    async def create_user_relationship(self, entity_name: str, relation: str, target_name: str):
        safe_relation = _sanitize_relationship(relation)
        query = f"""
        MERGE (e1:Entity {{name: $entity_name}})
        MERGE (e2:Entity {{name: $target_name}})
        MERGE (e1)-[r:{safe_relation}]->(e2)
        RETURN e1, r, e2
        """
        async with self.driver.session() as session:
            await session.run(query, entity_name=entity_name, target_name=target_name)
    
    async def get_user_context(self, entity_name: str):
        query = """
        MATCH (e1:Entity {name: $entity_name})-[r]->(e2:Entity)
        RETURN type(r) AS relationship, e2.name AS target
        """
        async with self.driver.session() as session:
            result = await session.run(query, entity_name=entity_name)
            records = await result.data()
            return records
        
    async def get_all_relationships(self):
        query = """
        MATCH (e1:Entity)-[r]->(e2:Entity)
        RETURN e1.name AS source, type(r) AS relation, e2.name AS target
        LIMIT 50
        """
        async with self.driver.session() as session:
            result = await session.run(query)
            records = await result.data()
            return records
        