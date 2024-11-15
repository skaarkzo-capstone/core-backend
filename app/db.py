import time
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

client = AsyncIOMotorClient(settings.database_url)
database = client[settings.MONGO_DB]

MAX_RETRIES = 3
RETRY_INTERVAL = 3


async def check_db_connection():
    for attempt in range(MAX_RETRIES):
        try:
            await client.admin.command("ping")      # Ping database to ensure it's running
            print("Connected to SustAIn's database successfully.")
            return
        except Exception as e:
            print(f"Attempt {attempt + 1} to connect to SustAIn's database failed: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_INTERVAL)
            else:
                print("Failed to connect to SustAIn's database after multiple retries.")
                raise
