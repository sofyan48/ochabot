import requests
import json


class Requester(object):
    def __init__(self):
        pass

    def post(self, url, payload):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': 'Bearer 30944132|8i36OMmQKAC6grpQ7rBozOPxOYz57LppPr3HTORx766c71d0',
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.text