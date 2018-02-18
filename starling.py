import requests
import json
from analytics import Analytics

class account:
    def __init__ (self,token):
        self.loggin = False
        self.token = token
        self.headers = {"Accept": "application/json","Content-Type": "application/json","Authorization": "Bearer "+token}
        self.processTransactions()

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

    def getTransactions(self):
        return self.get_req("https://api-sandbox.starlingbank.com/api/v1/transactions")

    def returnTransactions(self):
        data = self.getTransactions()
        transactions = data['_embedded']['transactions']
        for transaction in transactions:
            total += 1
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
            msg =  "This payment is for "+payment['reference'] + " for" + payment['recipientName'] + "of amount " + payment['amount']+"\n"
            speech += msg
        return speech
                       
    
    def processTransactions(self):
        transactions = (self.getTransactions())['_embedded']['transactions']
        transactions.reverse()
        self.analysis = Analytics(transactions)
        self.analysis.process()
        #return {"speech":speech, "action":"analysedTransactions"}
        
    # SAVING GOALS
    def getTotalInbound (self, day):
        return self.analysis.getTotalInbound(int(day))

    def returnTotalInbound (self, day):
        total = self.analysis.getTotalInBound (day)
        speech = "In " + day + "days " + "you received a total of: £ " + str(total)
        return {"speech":speech, "action":"returnTotalInBound"}


    def getTotalOutbound (self, day):
        return self.analysis.getTotalOutbound(int(day))

    def returnTotalOutbound (self, day):
        total = self.getTotalInbound(day)
        speech = "In " + day + "days " + "you spent a total of: £ " + str(total)
        return {"speech": speech, "action": "returnTotalOutbound"}

    def getAverageInbound (self, interval):
        return self.analysis.getAverageInbound(interval)

    def returnAverageInbound (self, interval):
        avg = self.analysis.getAverageInbound(int(interval))
        print("Average: ", avg)
        speech = "Over " + str(interval) + "days, you receive an average of: "  + str(avg)
        return {"speech":speech, "action":"returnAverageInbound"}

    def returnAverageOutbound (self, interval):
        avg = self.analysis.getAverageOutbound(int(interval))
        print("Average: ", avg)
        speech = "Over " + str(interval) + "days, you spend an average of: " + str(avg)
        return {"speech":speech, "action":"returnAverageOutbound"}


    def getAverageOutbound (self, interval):
        return self.analysis.getTotalOutbound(interval)

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
hughJass = account("wFaT0lPDGalC7GBqdacZ7aDYn5RhsDqW4wfrgPjYpd85xoTyijn8hnWzK6BAK4Si")
hughJass.processTransactions()
