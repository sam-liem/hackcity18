import requests

class account:
    def __init__ (self,token):
        self.loggin = False
        self.headers = {"Accept": "application/json","Content-Type": "application/json","Authorization": "Bearer "+token}

    def get_req(self, url):
        return requests.get(url, headers=self.headers).text

    def getBalance(self):
        return self.get_req("https://api-sandbox.starlingbank.com/api/v1/accounts/balance")

acc = account("1rxRXmg4lNh5rphevZwWNG1CYbTwRC9juFJe3ZGEenYo1wuStaXh2UZgMpNs9Pta")
print(acc.getBalance())
