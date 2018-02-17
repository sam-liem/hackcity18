import requests
import json

class account:
    def __init__ (self,token):
        self.loggin = False
        self.token = token
        self.headers = {"Accept": "application/json","Content-Type": "application/json","Authorization": "Bearer "+token}

    def get_req(self, url):
        return json.loads(requests.get(url, headers=self.headers).text)

    def getBalance(self):
        data = self.get_req("https://api-sandbox.starlingbank.com/api/v1/accounts/balance")
        speech = "You have "+str(data['effectiveBalance'])+" in your balance."
        return {"speech":speech,"action":"getBalance"}
