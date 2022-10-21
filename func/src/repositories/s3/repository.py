# Jormungandr - Onboarding
from ...infrastructures.s3.infrastructure import S3Infrastructure

# Standards
from tempfile import TemporaryFile

# Third party
from etria_logger import Gladsheim
from decouple import config


class FileRepository:

    infra = S3Infrastructure

    @classmethod
    async def save_user_file(cls, temp_file: TemporaryFile, file_path: str):
        try:
            bucket_name = config("AWS_BUCKET_USERS_FILES")
            async with cls.infra.get_client() as s3_client:
                await s3_client.upload_fileobj(
                    temp_file,
                    bucket_name,
                    file_path,
                )

        except Exception as ex:
            message = (
                f"Jormungandr-Onboarding::FileRepository::save_user_file:: error trying to save this user"
                f" selfie content {temp_file} and path {file_path}"
            )
            Gladsheim.error(error=ex, message=message)
            raise ex

    @classmethod
    async def list_contents(cls, file_path) -> dict:
        bucket_name = config("AWS_BUCKET_USERS_FILES")
        async with cls.infra.get_client() as s3_client:
            content_result = await s3_client.list_objects_v2(
                Bucket=bucket_name, Prefix=file_path
            )
            return content_result
