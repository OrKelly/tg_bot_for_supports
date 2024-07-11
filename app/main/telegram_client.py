import requests


class TelegramClient:
    def __init__(self, token, url):
        self.token = token
        self.url = url

    def prepare_url(self, method):
        result_url = f"{self.url}/bot{self.token}/"
        if method:
            result_url += method
        return result_url


    def post(self, method: str = None, params: dict = None, body: dict = None):
        url = self.prepare_url(method)
        resp = requests.post(url, params=params, data=body)
        return resp.json()