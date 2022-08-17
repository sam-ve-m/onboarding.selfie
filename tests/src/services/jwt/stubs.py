from enum import Enum


class SuccessResponse(Enum):
    SUCCESS = 0
    FAILURE = 1

stub_jwt_content = {
    "decoded_jwt": {"user": {"unique_id": "451baf5a-9cd5-4037-aa17-fbd0fcef66c8"}}
}

stub_heimdall_with_no_content = {}, SuccessResponse.SUCCESS
stub_heimdall_response = stub_jwt_content, SuccessResponse.SUCCESS
stub_heimdall_response_failure = "", SuccessResponse.FAILURE
