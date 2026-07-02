import asyncpg
import json
import datetime

DATABASE_URL = "postgresql://postgres:password@localhost:5432/persona_db"

async def init_db():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('''
        CREATE TABLE IF NOT EXIST events(
            id SERIAL PRIMARY KEY,
            event_type VARCHAR(255),
            description TEXT,
            timestamp TIMESTAMPTZ,
            metadata JSONB
        )
    ''')
    
async def store_event(event_type: str, description: str, metadata: dict):
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('''
        INSERT INTO events(event_type, description, timestamp, metadata)
        VALUES($1, $2, $3, $4)
    ''', event_type, description, datetime.datetime.now(datetime.timezone.utc), json.dumps(metadata))
    await conn.close()
    
async def get_recent_events(limit: int = 10):
    conn = await asyncpg.connect(DATABASE_URL)
    records = await conn.fetch('''
        SELECT id, event_type, description, timestamp
        FROM events
        ORDER BY timestamp DESC
        LIMIT $1
    ''', limit)
    await conn.close()
    
    return [dict(record) for record in records]