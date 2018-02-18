import json
import httpHelper
import csvHelper
from analytics import Analytics
class account:

    def __init__ (self,token):
        self.loggin = False
        self.token = token
        self.processTransactions()

    # TRANSER
    def transfer(self, recipientName, a, name ):
        dest = self.getContactFromName(recipientName)
        if (dest == {}):
            return {"speech":"Transfer failed, no account in your contacts with that name","action":"transfer"}
        destId = dest['id']

        data = {
                    "payment": {
                    "currency": "GBP",
                        "amount": a
                    },
                    "destinationAccountUid": destId,
                    "reference": name
                }

        res = httpHelper.post_req(self.token, "https://api-sandbox.starlingbank.com/api/v1/payments/local", data)
        speech = ""
        if res == {}:
            speech = "Transfer failed"
        else:
            speech = "Transfer success"

        return {"speech":speech,"action":"transfer"}

    # userInfo 
    def getUserInfo(self):
        accountData = self.getAccountData()
        cardData = httpHelper.get_req(self.token, "https://api-sandbox.starlingbank.com/api/v1/me")
        addressData = httpHelper.get_req(self.token, "https://api-sandbox.starlingbank.com/api/v1/addresses")
        balance = httpHelper.get_req(self.token, "https://api-sandbox.starlingbank.com/api/v1/accounts/balance")
        balance = balance['effectiveBalance']

        return {"accountData":accountData, "cardData":cardData, "addressData":addressData, "balance": balance}

    # CONTACTS
    def getContacts(self):
        contacts = httpHelper.get_req(self.token, "https://api-sandbox.starlingbank.com/api/v1/contacts")
        return contacts['_embedded']['contacts']

    def getContactFromName(self, name):
        contacts = self.getContacts()
        for contact in contacts:
            if (contact['name'] == name):
                return contact
        return {}

    # BALANCE
    def returnBalance(self):
        data = httpHelper.get_req(self.token, "https://api-sandbox.starlingbank.com/api/v1/accounts/balance")
        speech = "You have "+str(data['effectiveBalance'])+" in your balance."
        return {"speech":speech,"action":"returnBalance"}

    # ACCOUNT 
    def getAccountData(self):
        data = httpHelper.get_req(self.token, "https://api-sandbox.starlingbank.com/api/v1/accounts")
        return data

    def returnAccSort(self):
        data = self.getAccountData()
        speech = "Your sort code is "+str(data['sortCode'])+"."
        return {"speech":speech,"action":"returnSortCode"}

    def returnAccCurr(self):
        data = self.getAccountData()
        speech = "The currency of your account is "+str(data['currency'])+"."
        return {"speech":speech,"action":"returnSortCode"}

    def returnAccNumber(self):
        data = self.getAccountData()
        speech = "Your account number is "+str(data['number'])+"."
        return {"speech":speech,"action":"returnSortCode"}

    # TRANSACTIONS
    def getAllTransactions(self):
        data = httpHelper.get_req(self.token, "https://api-sandbox.starlingbank.com/api/v1/transactions")
        return data['_embedded']['transactions']

    def returnAllTransactions(self):
        return self.returnTransactions(self.getAllTransactions())

    def returnRecentTransaction(self):
        data = self.getAllTransactions()
        return self.returnTransactions([data[0]])

    def returnTransactions(self, data):
        transactions = data

        speech = ""
        for transaction in transactions:
            if transaction['direction'] == "OUTBOUND":
                msg = "Outbound transaction. Amount going out: " + str(transaction['amount']*-1) + " balance remaining: " + str(transaction['balance']) + " Date : " + str(transaction['created']) + "\n\n\n"
            else:
                msg = "Inbound transaction. Amount going in: " + str(transaction['amount']) + " balance remaining: " + str(transaction['balance']) + " Date : " + str(transaction['created']) + "\n\n\n"
            speech += msg

        return {"speech":speech, "action":"returnTransactions"}

    # PAYMENT SCHEDULES
    def getAllPaymentSchedules(self):
        data = httpHelper.get_req(self.token, "https://api-sandbox.starlingbank.com/api/v1/payments/scheduled")
        paymentOrders = data ['_embedded'] ['paymentOrders']
        return paymentOrders

    def returnAllPaymentSchedules(self):
        return self.returnPaymentSchedules(self.getAllPaymentSchedules())

    def returnPaymentSchedules(self, data):
        paymentOrders = data

        speech = ""
        for payment in paymentOrders:
            msg =  "This payment is for "+payment['reference'] + " for" + payment['recipientName'] + "of amount " + payment['amount']+"\n"
            speech += msg

        return {"speech":speech, "action":"returnPaymentSchedules"}

    # SAVING GOALS 
    def returnAllSavingsGoals(self):
        return self.returnSavingGoals(self.getAllSavingGoals())

    def returnSavingsGoals(self, data):
        savingGoals = data
        if savingGoals == {}:
            return {}

        savingGoals = savingGoals['savingsGoalList']

        speech = ""
        for savingGoal in savingGoals:
            targetAmount = int(savingGoal['target']['minorUnits'])
            savedAmount = int(savingGoal['totalSaved']['minorUnits'])
            percentageSaved = savedAmount / targetAmount
            msg = "For the "+ savingGoal['name'] + " savings goal, you've saved " + str(percentageSaved) + " percent."
            if (percentageSaved >= 1):
                msg = "You've reached your goal for " + savingGoal['name'] + "."
            elif (percentageSaved > 0.7):
                msg += " Keep going, you're only "+str(targetAmount-savedAmount)+" away."
            else: 
                msg += " Get saving, you're "+str(targetAmount-savedAmount)+" away. "
            speech += msg

        return {"speech":speech, "action":"returnSavingGoals"}

    def getAllSavingsGoals(self):
        data = httpHelper.get_req(self.token, "https://api-sandbox.starlingbank.com/api/v1/savings-goals")
        return data

    def addSavingsGoal(self, goalName, goalAmount):
        data = {
                  "name": goalName,
                  "currency": "GBP",
                  "target": {
                    "currency": "GBP",
                    "minorUnits": goalAmount
                  },
                  "totalSaved": {
                    "currency": "GBP",
                    "minorUnits": 0
                  },
                  "savedPercentage": 0
                }

        httpHelper.put_req(self.token, "https://api-sandbox.starlingbank.com/api/v1/savings-goals/b43d3060-2c83-4bb9-ac8c-c627b9c45f8b", data)
        speech = "You added a new savings goal: "+data['name'] + " for £" + str(data['target']['minorUnits']) + "!"
        return {"speech": speech, "action":"addSavingGoal"}

    def deleteSavingsGoal(self, goalName):
        savingGoals = self.getAllSavingGoals()
        if savingGoals == {}:
            return {"speech": "You have no saving goals!", "action":"deleteSavingGoal"}

        savingGoals = savingGoals['savingsGoalList']

        for savingGoal in savingGoals:
            if (savingGoal['name'] == goalName):
                sgId = savingGoal['_links']['photo']['href']
                if httpHelper.delete_req(self.token, "https://api-sandbox.starlingbank.com/"+sgId) == {}:
                    return {"speech": "Deleting " + goalName + " failed", "action":"deleteSavingGoal"}
                return {"speech": "Deleted " + goalName, "action":"deleteSavingGoal"}

        return {}

    def returnSavingsGoal(self, goalName):
        savingGoals = self.getAllSavingGoals()
        if savingGoals == {}:
            return {"speech": "You have no saving goals!", "action":"getSavingGoal"}

        savingGoals = savingGoals['savingsGoalList']

        for savingGoal in savingGoals:
            if (savingGoal['name'] == goalName):
                return self.returnSavingGoals({"savingsGoalList":[savingGoal]})

        return {"speech": "Couldn't find that goal!", "action":"returnSavingGoal"}

    # ANALYTICS
    def processTransactions(self):
        transactions = self.getAllTransactions()
        transactions.reverse()
        self.analysis = Analytics(transactions)
        self.analysis.process()
        # return {"speech":speech, "action":"analysedTransactions"}
    
    def getTotalInbound(self, day):
        return self.analysis.getTotalInbound(int(day))

    def returnTotalInbound(self, day):
        total = self.analysis.getTotalInBound(day)
        speech = "In " + day + "days " + "you received a total of: £ " + str(total)
        return {"speech": speech, "action": "returnTotalInBound"}

    def getTotalOutbound(self, day):
        return self.analysis.getTotalOutbound(int(day))

    def returnTotalOutbound(self, day):
        total = self.getTotalInbound(day)
        speech = "In " + day + "days " + "you spent a total of: £ " + str(total)
        return {"speech": speech, "action": "returnTotalOutbound"}

    def getAverageInbound(self, interval):
        return self.analysis.getAverageInbound(interval)

    def returnAverageInbound(self, interval):
        avg = self.analysis.getAverageInbound(int(interval))
        print("Average: ", avg)
        speech = "Over " + str(interval) + "days, you receive an average of: " + str(avg)
        return {"speech": speech, "action": "returnAverageInbound"}

    def returnAverageOutbound(self, interval):
        avg = self.analysis.getAverageOutbound(int(interval))
        print("Average: ", avg)
        speech = "Over " + str(interval) + "days, you spend an average of: " + str(avg)
        return {"speech": speech, "action": "returnAverageOutbound"}

    def getAverageOutbound(self, interval):
        return self.analysis.getTotalOutbound(interval)

    def setSpreadsheet(self):
        transactions = self.getAllTransactions()
        to_csv = csvHelper.to_csv(transactions)


#acc = account("1rxRXmg4lNh5rphevZwWNG1CYbTwRC9juFJe3ZGEenYo1wuStaXh2UZgMpNs9Pta")
#acc.getContactFromName("Heywood Floyd")
# hughJass = account("wFaT0lPDGalC7GBqdacZ7aDYn5RhsDqW4wfrgPjYpd85xoTyijn8hnWzK6BAK4Si")
# hughJass.processTransactions()
