# Jormungandr - Onboarding
from ..base_repository.base import MongoDbBaseRepository

# Third party
from etria_logger import Gladsheim


class UserRepository(MongoDbBaseRepository):
    @classmethod
    async def update_one(
        cls, unique_id: str, update: dict
    ):
        collection = await cls._get_collection()
        try:
            user_updated = await collection.update_one(
                {"unique_id": unique_id}, {"$set": update}
            )
            return user_updated
        except Exception as ex:
            message = f'UserRepository::update_one::error on updating":{update}'
            Gladsheim.error(error=ex, message=message)
            raise ex
