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
        print(r.text)
        if (r.status_code != 200):
            return {}
        else:
            return json.loads(r.text)

    def put_req(self, url, d):
        r = requests.put(url, headers=self.headers, data=json.dumps(d))
        print(r.text)
        if (r.status_code != 200):
            return {}
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

    def returnTransactions(self):
        data = self.get_req("https://api-sandbox.starlingbank.com/api/v1/transactions")

        transactions = data['_embedded']['transactions']

        speech = ""
        for transaction in transactions:
            if transaction['direction'] == "OUTBOUND":
                msg = "Outbound transaction. Amount going out: " + str(transaction['amount']*-1) + " balance remaining: " + str(transaction['balance']) + " Date : " + str(transaction['created']) + "\n"
            else:
                msg = "Inbound transaction. Amount going in: " + str(transaction['amount']) + " balance remaining: " + str(transaction['balance']) + " Date : " + str(transaction['created']) + "\n"
            speech += msg

        return {"speech":speech, "action":"returnTransactions"}

    # SAVING GOALS 
    def returnAllSavingGoals(self):
        return self.returnSavingGoals(self.getAllSavingGoals())

    def returnSavingGoals(self, data):
        savingGoals = data
        if savingGoals == {}:
            return {}

        savingGoals = savingGoals['savingsGoalList']

        speech = ""
        for savingGoal in savingGoals:
            targetAmount = int(savingGoal['target']['minorUnits'])
            savedAmount = int(savingGoal['totalSaved']['minorUnits'])
            percentageSaved = savedAmount / targetAmount
            msg = "You've saved " + str(percentageSaved) + " percent of your " + savingGoal['name'] + " fund!"
            if (percentageSaved >= 1):
                msg = "You've reached your goal for " + savingGoal['name'] + "."
            elif (percentageSaved > 0.7):
                msg += " Keep going, you're only "+str(targetAmount-savedAmount)+" away."
            else: 
                msg += " Get saving, you're "+str(targetAmount-savedAmount)+" away. "
            speech += msg

        return {"speech":speech, "action":"returnSavingGoals"}

    def getAllSavingGoals(self):
        data = self.get_req("https://api-sandbox.starlingbank.com/api/v1/savings-goals")
        return data

    def addSavingGoal(self, data):
        # handle data after dialogflow is setup
        # TODO
        data = {
                  "name": "Trip to Paris",
                  "currency": "GBP",
                  "target": {
                    "currency": "GBP",
                    "minorUnits": 11223344
                  },
                  "totalSaved": {
                    "currency": "GBP",
                    "minorUnits": 2
                  },
                  "savedPercentage": 50
                }
        self.put_req("https://api-sandbox.starlingbank.com/api/v1/savings-goals/b43d3060-2c83-4bb9-ac8c-c627b9c45f8b", data)
        speech = "You added a new savings goal: "+data['name'] + " for " + str(data['target']['minorUnits'])
        return {"speech": speech, "action":"addSavingGoal"}

    def deleteSavingGoal(self, goalName):
        savingGoals = self.getAllSavingGoals()
        if savingGoals == {}:
            return {"speech": "You have no saving goals!", "action":"deleteSavingGoal"}

        savingGoals = savingGoals['savingsGoalList']

        for savingGoal in savingGoals:
            if (savingGoal['name'] == goalName):
                sgId = savingGoal['photo']['href']
                self.delete_req("https://api-sandbox.starlingbank.com/"+sgId)
                return {"speech": "Deleted " + goalName, "action":"deleteSavingGoal"}

        return {}

    def returnSavingGoal(self, goalName):
        savingGoals = self.getAllSavingGoals()
        if savingGoals == {}:
            return {"speech": "You have no saving goals!", "action":"getSavingGoal"}

        savingGoals = savingGoals['savingsGoalList']

        for savingGoal in savingGoals:
            if (savingGoal['name'] == goalName):
                return self.returnSavingGoals({"savingsGoalList":[savingGoal]})

        return {"speech": "Couldn't find that goal!", "action":"getSavingGoal"}

acc = account("1rxRXmg4lNh5rphevZwWNG1CYbTwRC9juFJe3ZGEenYo1wuStaXh2UZgMpNs9Pta")
