from datetime import datetime
from app.db import database


async def seed_companies():
    companies_collection = database["companies"]
    evaluated_companies_collection = database["evaluated_companies"]

    companies = [
        {
            "name": "Smith Construction Ltd.",
        },
        {
            "name": "Maple Foods Inc.",
        },
        {
            "name": "Urban Outfitters Co.",
        },
        {
            "name": "Horizon Hospitality Group",
        },
        {
            "name": "No Scraped Data Company",
        },
    ]

    evaluated_companies = [
        {
            "name": "Smith Construction Ltd.",
            "date": datetime.utcnow(),
            "score": 85,
            "reasoning": "Great performance in Q3",
        },
        {
            "name": "Maple Foods Inc.",
            "date": datetime.utcnow(),
            "score": 72,
            "reasoning": "Consistent revenue growth",
        },
        {
            "name": "Urban Outfitters Co.",
            "date": datetime.utcnow(),
            "score": 65,
            "reasoning": "Improved operations",
        },
        {
            "name": "Horizon Hospitality Group",
            "date": datetime.utcnow(),
            "score": 65,
            "reasoning": "Better guest satisfaction",
        },
    ]

    try:
        await companies_collection.delete_many({})
        await evaluated_companies_collection.delete_many({})

        companies_result = await companies_collection.insert_many(companies)
        print(f"Inserted IDs: {companies_result.inserted_ids}")

        evaluated_companies_result = await evaluated_companies_collection.insert_many(evaluated_companies)
        print(f"Inserted IDs: {evaluated_companies_result.inserted_ids}")
    except Exception as e:
        print(f"Error seeding companies: {e}")
        print(f"Error seeding evaluated companies: {e}")
