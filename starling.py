import requests
import json

class account:
    def __init__ (self,token):
        self.loggin = False
        self.token = token
        self.headers = {"Accept": "application/json","Content-Type": "application/json","Authorization": "Bearer "+token}

    def get_req(self, url):
        return json.loads(requests.get(url, headers=self.headers).text)

    def returnBalance(self):
        data = self.get_req("https://api-sandbox.starlingbank.com/api/v1/accounts/balance")
        speech = "You have "+str(data['effectiveBalance'])+" in your balance."
        return {"speech":speech,"action":"returnBalance"}

    def getAcc(self):
        data = self.get_req("https://api-sandbox.starlingbank.com/api/v1/accounts")
        return data

    def returnAccSort(self):
        accountData = self.getAccountData()
        speech = "Your sort code is "+str(data['sortCode'])+"."
        return {"speech":speech,"action":"returnSortCode"}

    def returnAccCurr(self):
        accountData = self.getAccountData()
        speech = "The currency of your account is "+str(data['currency'])+"."
        return {"speech":speech,"action":"returnSortCode"}

    def returnAccNumber(self):
        accountData = self.getAccountData()
        speech = "Your account number is "+str(data['number'])+"."
        return {"speech":speech,"action":"returnSortCode"}


