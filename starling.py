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

    def put_req(self, url, d):
        r = requests.put(url, headers=self.headers, data=json.dumps(d))
        print(r.content)
        if (r.status_code != 200):
            return {}
        else:
            return json.loads(r.text)

    def post_req (self, url, d):
        r = reuests.post(url, headers=self.headers, data=json.dumps(d))
        print(r.text)
        if status_code != 200:
            return []
        else:
            return json.loads(r.text)
              
    def delete_req(self, url):
        r = requests.delete(url, headers=self.headers)
        return {}

    # BALANCE
    def returnBalance(self):
        data = self.get_req("https://api-sandbox.starlingbank.com/api/v1/accounts/balance")
        speech = "You have "+str(data['effectiveBalance'])+" in your balance."
        return {"speech":speech,"action":"returnBalance"}

    # ACCOUNT 
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

    def getTransactions(self):
        transactions = data['_embedded']['transactions']

        speech = ""
        for transaction in transactions:
            if transaction['direction'] == "OUTBOUND":
                msg = "Outbound transaction. Amount going out: " + str(transaction['amount']*-1) + " balance remaining: " + str(transaction['balance']) + " Date : " + str(transaction['created']) + "\n"
            else:
                msg = "Inbound transaction. Amount going in: " + str(transaction['amount']) + " balance remaining: " + str(transaction['balance']) + " Date : " + str(transaction['created']) + "\n"
            speech += msg

        return {"speech":speech, "action":"returnTransactions"}

    def getPaymentSchedules(self):
        data = self.get_req("https://api-sandbox.starlingbank.com/api/v1/payments/scheduled")
        paymentOrders = data ['_embedded'] ['paymentOrders']

        speech = ""
        for payment in paymentOrders:
            msg = " ".join ("This payment is for",payment['reference'],
                            "for",payment['recipientName'],"of amount",
                            payment['amount'],"\n")
            speech += msg

            

        return speech
                       
    

    # SAVING GOALS 
    def getSavingGoals(self):
        data = self.get_req("https://api-sandbox.starlingbank.com/api/v1/savings-goals")
        return data

    def addSavingGoal(self, data):
        data = {
               "name": "Trip to Paris",
                   "target": {
                     "currency": "GBP",
                     "minorUnits": 11223344
                   },
                   "totalSaved": {
                     "currency": "GBP",
                     "minorUnits": 11223344
                   },
                   "savedPercentage": 50
                 }
        self.put_req("https://api-sandbox.starlingbank.com/api/v1/savings-goals/e43d3060-2c83-4bb9-ac8c-c627b9c45f8b", data)
        # print(self.getSavingGoals())

acc = account("1rxRXmg4lNh5rphevZwWNG1CYbTwRC9juFJe3ZGEenYo1wuStaXh2UZgMpNs9Pta")

