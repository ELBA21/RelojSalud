import motor.motor_asyncio
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient
from app.config import DatabaseConfig


class MongoDBConnectionManager:
    def __init__(self) -> None:
        self.uri: str = DatabaseConfig.uri
        self.db_name: str = DatabaseConfig.name
        self.db: AsyncIOMotorDatabase | None = None
        self.client: AsyncIOMotorClient | None = None

    async def __aenter__(self) -> AsyncIOMotorDatabase:
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.uri)
        self.db = self.client[self.db_name]
        return self.db

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        _ = exc_type, exc_val, exc_tb
        if self.client:
            self.client.close()


async def mongo_connection_check() -> None:
    """Verify MongoDB connectivity; raise 500 if unavailable."""
    try:
        async with MongoDBConnectionManager() as db:
            await db.command("ping")
    except Exception as e:
        raise RuntimeError(f"Database connection failed: {e}")
