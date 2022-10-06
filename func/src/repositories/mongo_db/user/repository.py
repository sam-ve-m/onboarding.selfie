from contextlib import contextmanager

from decouple import config
from etria_logger import Gladsheim

from src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure


class UserRepository:
    infra = MongoDBInfrastructure

    @classmethod
    @contextmanager
    def __get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            database = mongo_client[config("MONGODB_DATABASE_NAME")]
            collection = database[config("MONGODB_USER_COLLECTION")]
            yield collection
        except Exception as error:
            message = 'MongoDbBaseRepository::collection::error on operating collection'
            Gladsheim.error(error=error, message=message)
            raise error
        finally:
            del collection
            del database

    @classmethod
    async def update_one(
        cls, unique_id: str, update: dict
    ):
        with cls.__get_collection() as collection:
            user_updated = await collection.update_one(
                {"unique_id": unique_id}, {"$set": update}
            )
            return user_updated
