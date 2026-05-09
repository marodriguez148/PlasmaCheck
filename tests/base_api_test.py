import requests


class BaseAPITest:
    def setup_method(self):
        self.host = "https://stage-api.ezra.com"

    def teardown_method(self) -> None:
        pass

    def request(
        self, method: str, endpoint: str, token: str = None, **kwargs
    ) -> requests.Response:
        url = f"{self.host}{endpoint}"
        headers = kwargs.pop("headers", {})
        if token:
            headers["Authorization"] = f"Bearer {token}"
        return requests.request(method, url, headers=headers, **kwargs)
