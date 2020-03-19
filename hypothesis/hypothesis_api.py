import requests

class Api:
    base_url ="https://api.hypothes.is/api"

    def __init__(self,bearer_token):
        self.header = {'Authorization': 'Bearer ' + bearer_token}
        response = requests.get(self.base_url, headers=self.header)
        self.urls = response.json()