import requests


class Request:

    def __init__(self, url):

        self.url = url

    
    def get(self):

        return requests.get(self.url)

    
    def head(self):

        return requests.head(self.url)