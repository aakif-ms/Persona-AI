from neo4j import AsyncGraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "password123"

class SemanticMemory:
    def __init__(self):
        self.driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    
    async def close(self):
        await self.driver.close()
    
    async def create_user_relationship(self, entity_name: str, relation: str, target_name: str):
        query = f"""
        MERGE (e1:Entity {{name: $entity_name}})
        MERGE (e2:Entity {{name: $target_name}})
        MERGE (e1)-[r:{relation}]->(e2)
        RETURN e1, r, e2
        """
        async with self.driver.session() as session:
            await session.run(query, entity_name=entity_name, target_name=target_name)4
    
    async def get_user_context(self, entity_name: str):
        query = """
        MATCH (e1:Entity {name: $entity_name})-[r]->(e2:Entity)
        RETURN type(r) AS relationship, e2.name AS target
        """
        async with self.driver.session() as session:
            result = await session.run(query, entity_name=entity_name)
            records = await result.data()
            return records