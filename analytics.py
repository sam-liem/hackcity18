
from datetime import datetime
import random
import operator


class Accumulation(object):
    def __init__(self, day, cumulative_total, balance, dateRef):
        self.day_num = day
        self.cumulative_total = cumulative_total
        self.balance = balance
        self.dateRef = dateRef
        
class Analytics(object):
    def __init__ (self, transactions):
         self.transactions = transactions
         self.outbounds = []
         self.inbounds = []
         self.outbounds_cumulative = []
         self.inbounds_cumulative = []
         self.processed = False
    

    #Get a datetime object based on the first data and time noticed
    def getBaseDate (self):
        date = self.transactions[0]['created']
        date = date[0:date.index(".")]
        date = list(date)
        date[date.index("T")] = '-'
        for i in range(2):
            date[date.index(":")] = '-'
        date = ''.join(date)
        #format: yyyy-mm-ddThh-mm-ss
        tokens = date.split("-")
        datetimeObj = datetime(int(tokens[0]),
                               int(tokens[1]),
                               int(tokens[2]),
                               int(tokens[3]),
                               int(tokens[4]),
                               int(tokens[5]))

        return datetimeObj
                                
    def alterDates (self):
        random.seed(1)
        dateObj = self.getBaseDate()
        self.transactions[0]['created'] = dateObj
      
        for trans in range(1,len(self.transactions)):
            dateObj = self.transactions[trans-1]['created']
            seconds = dateObj.timestamp()
            rand = self.getRandomTime()
            self.transactions[trans]['created'] = datetime.fromtimestamp(rand+seconds)
            if self.transactions[trans]['direction'] == "OUTBOUND":
                self.outbounds += [self.transactions[trans]['direction']]

            else:
                self.inbounds += [self.transactions[trans]['direction']]

        for trans in self.transactions:
            print ("Date: ", trans['created']," type: ", trans['direction'], "amount: ", trans['amount'])
        
    def getRandomTime(self):
        fiveMinutes = 300
        twoDays = 172800
        fiveDays = 432000
        tenDays = 864000
        
        #90% chance picking between 300 seconds and five days
        num = random.randint(1,100)
        if num < 80 :
            return  random.randint (fiveMinutes, twoDays)

        elif num < 95:
            return random.randint (twoDays, fiveDays)

        else:
            return random.randint (fiveDays, tenDays)

    def process (self):
        self.analyse()

    def getInbounds (self, days):
        pass

    def getOutbounds (self, days):
        pass
    def analyse(self):
        self.alterDates()
        day = 0
        inboundTotal = 0
        outboundTotal = 0
        mostRecent = None
        #I get the cumulative inbound and outbounds
        #The interval will be one day
        for trans in range(len(self.transactions)):
            balance = self.transactions[trans]['balance']
            currDate = self.transactions[trans]['created']
            cash_diff = self.transactions[trans]['amount']
            if self.transactions[trans]['direction'] == "OUTBOUND":
                cash_diff *= -1
                outboundTotal += cash_diff
                if self.outbounds_cumulative == []:
                    if mostRecent != None:
                        day += (currDate - mostRecent['creative']).days

                    self.outbounds_cumulative += [Accumulation(day,outboundTotal,balance,currDate)]

                else:
                    prev = self.outbounds_cumulative[-1].dateRef

                    if (currDate.year == prev.year and
                        currDate.month == prev.month and
                        currDate.day == prev.day):
                        self.outbounds_cumulative[-1].cumulative_total = outboundTotal
                        self.outbounds_cumulative[-1].balance = balance

                    else:
                        day += (currDate - mostRecent['created']).days
                        self.outbounds_cumulative += [Accumulation(day,outboundTotal,balance,currDate)]
            else:
                inboundTotal += cash_diff
                if self.inbounds_cumulative == []:
                    if mostRecent != None:
                        day += (currDate - mostRecent['created']).days
                        self.inbounds_cumulative += [Accumulation(day,inboundTotal,balance,currDate)]

                else:
                    prev = self.inbounds_cumulative[-1].dateRef

                    if (currDate.year == prev.year and
                        currDate.month == prev.month and
                        currDate.day == prev.day):
                        self.inbounds_cumulative[-1].cash_difference = inboundTotal
                        self.inbounds_cumulative[-1].balance = balance

                    else:
                        day += (currDate - mostRecent['created']).days
                        self.inbounds_cumulative += [Accumulation(day,inboundTotal,balance,currDate)]

            mostRecent = self.transactions[trans]
        self.processed = True


        print ("Getting inbounds accumulation: ")
        for trans in self.inbounds_cumulative:
            print ("Day: " , trans.day_num , " total: ", trans.cumulative_total)


        print ("Getting outbounds accumulation: ")
        for trans in self.outbounds_cumulative:
            print("Day: ", trans.day_num, " total: ", trans.cumulative_total)


    def highestExpense(self, transactions):
        transactions = transactions['_embedded']['transactions']

        # get most recent month's transactions?
        narrativeCostTable = {}
        for transaction in transactions:
            if (transaction['direction'] == "OUTBOUND") and (transaction['narrative'] != "External Payment") and (transaction['narrative'] != "Mastercard"):
                if (transaction['narrative'] in narrativeCostTable):
                    narrativeCostTable[transaction['narrative']] += int(transaction['amount'])
                else:
                    narrativeCostTable[transaction['narrative']] = int(transaction['amount'])

        narrativeCostTable = sorted(narrativeCostTable.items(), key=operator.itemgetter(1))

        name, spent = narrativeCostTable[0]
        speech = "You spent " + str(spent * -1) + " on " + name + ". Consider switching to cheaper alternatives."
        print(speech)

