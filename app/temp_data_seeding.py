from datetime import datetime
from app.db import database

async def seed_companies():
    collection = database["evaluated_companies"]

    companies = [
        {
            "name": "Google",
            "date": datetime.utcnow(),
            "score": 85,
            "reasoning": "Great performance in Q3",
        },
        {
            "name": "Microsoft",
            "date": datetime.utcnow(),
            "score": 72,
            "reasoning": "Consistent revenue growth",
        },
        {
            "name": "Amazon",
            "date": datetime.utcnow(),
            "score": 65,
            "reasoning": "Improved operations",
        },
    ]

    try:
        await collection.delete_many({})
        result = await collection.insert_many(companies)
        print(f"Inserted IDs: {result.inserted_ids}")
    except Exception as e:
        print(f"Error seeding companies: {e}")
