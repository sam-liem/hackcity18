import requests
import json

class account:
    def __init__ (self,token):
        self.loggin = False
        self.token = token
        self.headers = {"Accept": "application/json","Content-Type": "application/json","Authorization": "Bearer "+token}

    # REQUEST functions
    def get_req(self, url):
        r = requests.get(url, headers=self.headers)
        if (r.status_code != 200):
            return {}
        else:
            return json.loads(r.text)

    # BALANCE
    def returnBalance(self):
        data = self.get_req("https://api-sandbox.starlingbank.com/api/v1/accounts/balance")
        speech = "You have "+str(data['effectiveBalance'])+" in your balance."
        return {"speech":speech,"action":"returnBalance"}

    # ACCOUNT information
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


    def getPaymentSchedules(self):
        data = self.get_req("https://api-sandbox.starlingbank.com/api/v1/payments/scheduled")
        #paymentOrders = data ['paymentOrders']

        print(data)

acc = account("1rxRXmg4lNh5rphevZwWNG1CYbTwRC9juFJe3ZGEenYo1wuStaXh2UZgMpNs9Pta")
acc.getPaymentSchedules()