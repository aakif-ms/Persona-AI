import os
import json
import datetime

import asyncpg

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:password@localhost:5432/persona_db",
)

async def init_db():
    try:
        conn = await asyncpg.connect(DATABASE_URL)
    except Exception as exc:
        print(f"Database unavailable: {exc}")
        return False

    try:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS events(
                id SERIAL PRIMARY KEY,
                event_type VARCHAR(255),
                description TEXT,
                timestamp TIMESTAMPTZ,
                metadata JSONB
            )
            """
        )
    finally:
        await conn.close()

    return True


async def store_event(event_type: str, description: str, metadata: dict):
    try:
        conn = await asyncpg.connect(DATABASE_URL)
    except Exception as exc:
        print(f"Unable to store event: {exc}")
        return False

    try:
        await conn.execute(
            """
            INSERT INTO events(event_type, description, timestamp, metadata)
            VALUES($1, $2, $3, $4)
            """,
            event_type,
            description,
            datetime.datetime.now(datetime.timezone.utc),
            json.dumps(metadata),
        )
    except Exception as exc:
        print(f"Unable to store event: {exc}")
        return False
    finally:
        await conn.close()

    return True


async def get_recent_events(limit: int = 10):
    try:
        conn = await asyncpg.connect(DATABASE_URL)
    except Exception as exc:
        print(f"Unable to load recent events: {exc}")
        return []

    try:
        records = await conn.fetch(
            """
            SELECT id, event_type, description, timestamp
            FROM events
            ORDER BY timestamp DESC
            LIMIT $1
            """,
            limit,
        )
    except Exception as exc:
        print(f"Unable to load recent events: {exc}")
        return []
    finally:
        await conn.close()

    return [dict(record) for record in records]