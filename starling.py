import requests
import json


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


    def getTransactions(self):
        data = self.get_req("https://api-sandbox.starlingbank.com/api/v1/transactions/any")

        transactions = data['transactions']

        speech = ""
        for transaction in transaction:
            if transaction['direction'] == "OUTBOUND":
                msg = "Outbound transaction. Amount going out: " + str(transaction['amount']*-1) +" balance remaining: " + str(transaction['balance']) + " Date : " + str(transaction['created']) + "\n"

            else:
                msg = "Inbound transaction. Amount going in: " + str(transaction['amount']) + " balance remaining: " + str(transaction['balance']) + " Date : " + str(transaction['created']) + "\n"

            speech += msg

        return {"speech":speech, "action":"returnTransactions"}


    def getPaymentSchedules(self):
        data = self.get_req("https://api-sandbox.starlingbank.com/api/v1/payments/scheduled")
        #paymentOrders = data ['paymentOrders']

        print(data)
                                                         

    
                          
                

 

       
