import unittest
from unittest.mock import patch

from memory import episodic_memory


class EpisodicMemoryTests(unittest.IsolatedAsyncioTestCase):
    async def test_init_db_returns_false_when_database_is_unavailable(self):
        with patch("memory.episodic_memory.asyncpg.connect", side_effect=ConnectionError("db unavailable")):
            result = await episodic_memory.init_db()

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
