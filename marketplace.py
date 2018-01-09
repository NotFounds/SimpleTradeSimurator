import requests

class MarketPlace():
    def __init__(self, uri):
        self.uri = uri
        self.session = requests.session()

    def get(self, url):
        return self.session.get(self.uri + url).json()