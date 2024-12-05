from app.db import database


# TODO: Delete when proper deleting evaluating companies is added.
async def delete_companies():
    companies_collection = database["companies"]
    evaluated_companies_collection = database["evaluated_companies"]

    try:
        await companies_collection.delete_many({})
        await evaluated_companies_collection.delete_many({})
    except Exception as e:
        print(f"Error seeding companies: {e}")
        print(f"Error seeding evaluated companies: {e}")
