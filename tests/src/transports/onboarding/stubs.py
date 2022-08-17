stub_payload = {
    "result": {
        "current_step": "selfie"
    }
}


class RequestStub:
    def __init__(self, status_code: int = None):
        self.status_code = status_code
        self.json = self.json

    @staticmethod
    def json():
        return stub_payload


stub_request_success = RequestStub(status_code=200)
stub_request_failure = RequestStub(status_code=500)

print(stub_request_success.status_code)
